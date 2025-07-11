import unittest
from dotenv import load_dotenv
import os
import random
import aioftp
from ..ftp_client_exceptions import ClientFileNotFoundError, ClientNoPathProvidedError
from ..uploader import Uploader

class TestUploader(unittest.IsolatedAsyncioTestCase):
    async def connect(self): # Create a dummy aioftp client
        load_dotenv("public.env")
        aioClient = aioftp.Client()
        await aioClient.connect(os.getenv("ip"), os.getenv("port"))
        await aioClient.login("user", "password")
        print(f"Test client connected to {os.getenv("ip")}:{os.getenv("port")}")
        print("Ready.")
        return aioClient
    def find_paths(self, directory: str) -> list: # Return array of paths in a given directory
        paths = []
        for file in os.listdir(directory):
            paths.append(os.path.join(directory, file))
        return paths
    def generate_files(self): # Generate random files in local and remote
        i = random.randint(3, 8)
        while i > 0:
            with open(f"local/local_{i}.txt", "w") as file:
                file.write("I am a file!")
            with open(f"remote/remote_{i}.txt", "w") as file:
                file.write("I am a file too!")
            i -= 1
        return
    def cleanup_files(self): # Cleanup files after we're done
        localPaths = self.find_paths("local")
        remotePaths = self.find_paths("remote")
        all = localPaths + remotePaths
        for path in all:
            if(os.path.exists(path) and "local_" in path or "remote_" in path):
                os.remove(path)

    async def test_perform_upload_file(self):
        client = await self.connect() # Connect aioftp 
        self.generate_files() # Generate files in local/remote

        # Find file paths for each
        local_dir = self.find_paths("local")

        uploaded = 0 # Files we uploaded from local dir
        found = 0 # Files we found in remote dir
        for file_path in local_dir:
            if "local_" in file_path:
                uploader = Uploader(client, path=file_path)
                assert await uploader.perform_upload() == 1
                uploaded += 1

        remote_dir = self.find_paths("remote")
        for file_path in remote_dir:
            if "local_" in file_path:
                assert os.path.exists(file_path)
                found += 1
        assert uploaded == found # Assert that the number of files we upload == number of local_ files on remote
        self.cleanup_files()

    async def test_perform_upload_directory(self):
        client = await self.connect() # Connect
        os.makedirs("local/local_folder") # Create folder
        uploader = Uploader(client, "local/local_folder") 
        assert await uploader.perform_upload() == 1 # upload complete
        assert os.path.exists("remote/local_folder") # folder exists on remote?
        os.removedirs("local/local_folder")
        os.removedirs("remote/local_folder")

    async def test_perform_download_file(self):
        client = await self.connect()
        self.generate_files()
        downloaded = 0
        found = 0
        remote_dir = self.find_paths("remote")
        for file_path in remote_dir:
            if "remote_" in file_path:
                uploader = Uploader(client, file_path.split("remote\\")[1]) # Hack the path to be relative
                assert await uploader.perform_download() == 1
                downloaded += 1

        local_dir = self.find_paths("local")
        for file_path in local_dir:
            if "remote_" in file_path:
                assert os.path.exists(file_path)
                found += 1
        assert found == downloaded
        print("cleaning up!")
        self.cleanup_files()

    async def test_perform_download_directory(self):
        client = await self.connect()
        os.makedirs("remote/remote_folder")
        uploader = Uploader(client, "remote_folder")
        assert await uploader.perform_download() == 1
        assert os.path.exists("local/remote_folder")
        os.removedirs("remote/remote_folder")
        os.removedirs("local/remote_folder")

    async def test_perform_download_no_file_path(self):
        uploader = Uploader(None)
        with self.assertRaises(ClientNoPathProvidedError):
            await uploader.perform_download()
    
    async def test_perform_download_no_file_found(self):
        client = await self.connect()
        uploader = Uploader(client, path="klasjdfklasjdflkadjfl.txt")
        with self.assertRaises(ClientFileNotFoundError):
            await uploader.perform_download()

    async def test_perform_upload_no_file_path(self):
        uploader = Uploader(None)
        with self.assertRaises(ClientNoPathProvidedError):
            await uploader.perform_upload()
        
    async def test_perform_upload_no_file_found(self):
        fpath = "ewrgvwretgherhwer.txt"
        file_uploader = Uploader(None, path=fpath)
        with self.assertRaises(ClientFileNotFoundError):
            await file_uploader.perform_upload()
    
    async def test_perform_upload_no_dir_found(self):
        fpath = "complete/nonsense/fpath/with/no/end"
        dir_uploader = Uploader(None, path=fpath)
        with self.assertRaises(ClientFileNotFoundError):
            await dir_uploader.perform_upload()
