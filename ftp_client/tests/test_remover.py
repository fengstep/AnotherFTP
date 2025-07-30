import unittest
from dotenv import load_dotenv
import os
import random
import aioftp
from ..ftp_client_exceptions import DirectoryDoesNotExistError
from ..uploader import Uploader
from ..creator import Creator
from ..remover import Remover

class TestCreator(unittest.IsolatedAsyncioTestCase):
    async def connect(self):
        """
        Virtualized test FTP
        """
        load_dotenv("public.env")
        aio_client = aioftp.Client()
        await aio_client.connect(os.getenv("ip"), os.getenv("port"))
        await aio_client.login("user", "password")
        return aio_client
    
    async def test_removing_directory_that_does_not_exist(self):
        """
        Try to remove a directory that does not exist.
        Should raise DirectoryDoesNotExistError.
        """
        test_client = await self.connect()
        name_to_remove = "test_non_existent_directory_total_gibberish"
        test_remover = Remover(test_client)
        with self.assertRaises(DirectoryDoesNotExistError):
            await test_remover.remove_file(name_to_remove)

    async def test_removing_directory_that_exists(self):
        """
        Create a directory, then remove it.
        Should not raise any exceptions.
        """
        test_client = await self.connect()
        name_to_create = "test_directory"
        test_creator = Creator(test_client)
        await test_creator.create_directory(name_to_create)
        
        test_remover = Remover(test_client)
        await test_remover.remove_file(name_to_create)
        assert not await test_client.exists(name_to_create), "Directory should have been removed"

    async def test_removing_file_that_exists(self):
        """
        Create a file, then remove it.
        Should not raise any exceptions.
        """
        test_client = await self.connect()
        name_to_create = "test_file.txt"
        with open(name_to_create, "w") as f:
            f.write("This is a test file.")
        
        test_uploader = Uploader(test_client, path=name_to_create)
        await test_uploader.perform_upload()
        
        test_remover = Remover(test_client)
        await test_remover.remove_file(name_to_create)
        
        assert not await test_client.exists(name_to_create), "File should have been removed"