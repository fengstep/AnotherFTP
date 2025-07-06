import asyncio
import unittest
import os
from .ftp_client import run_client
from .ftp_client_exceptions import ClientFileNotFoundError, ClientNoFilePathError
from .uploader import Uploader

class TestUploader(unittest.TestCase):

    @unittest.skip("Needs online implementation")
    def test_perform_upload_file(self):
        fpath = os.path.abspath("testing_assets/huh_cat.gif")
        uploader = Uploader(None, path_to_file=fpath)
        assert(os.path.exists("../huh_cat.gif"))

    @unittest.skip("Needs online implementation")
    def test_perform_upload_directory(self):
        fpath = os.path.abspath("testing_assets/stuff_folder")
        uploader = Uploader(None, path_to_dir=fpath)
        assert(os.path.exists("../stuff_folder"))

    async def test_perform_upload_no_file_path(self):
        uploader = Uploader(None)
        with self.assertRaises(ClientNoFilePathError):
            await uploader.perform_upload()
        
    async def test_perform_upload_no_file_found(self):
        fpath = "ewrgvwretgherhwer.txt"
        file_uploader = Uploader(None, path_to_file=fpath)
        with self.assertRaises(ClientFileNotFoundError):
            await file_uploader.perform_upload()
    
    async def test_perform_upload_no_dir_found(self):
        fpath = "complete/nonsense/fpath/with/no/end"
        dir_uploader = Uploader(None, path_to_dir=fpath)
        with self.assertRaises(ClientFileNotFoundError):
            await dir_uploader.perform_upload()
