import asyncio
import unittest
import os
from ..ftp_client_exceptions import ClientFileNotFoundError, ClientNoPathProvidedError
from ..uploader import Uploader

class TestUploader(unittest.IsolatedAsyncioTestCase):

    @unittest.skip("Needs online implementation")
    def test_perform_upload_file(self):
        fpath = os.path.abspath("testing_assets/huh_cat.gif")
        uploader = Uploader(None, path=fpath)
        assert(os.path.exists("../huh_cat.gif"))

    @unittest.skip("Needs online implementation")
    def test_perform_upload_directory(self):
        fpath = os.path.abspath("testing_assets/stuff_folder")
        uploader = Uploader(None, path=fpath)
        assert(os.path.exists("../stuff_folder"))

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
