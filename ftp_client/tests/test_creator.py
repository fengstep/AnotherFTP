import unittest
from dotenv import load_dotenv
import os
import random
import aioftp
from ..ftp_client_exceptions import DirectoryAlreadyExistsError
from ..uploader import Uploader
from ..creator import Creator
from ..remover import Remover

class TestCreator(unittest.IsolatedAsyncioTestCase):
    async def connect(self):
        load_dotenv("public.env")
        aio_client = aioftp.Client()
        await aio_client.connect(os.getenv("ip"), os.getenv("port"))
        await aio_client.login("user", "password")
        return aio_client
    
    async def test_creating_directory_that_already_exists(self):
        """
        Create a directory, then try to create it again.
        Should raise DirectoryAlreadyExistsError.
        """
        test_client = await self.connect()
        name_to_create = "test_directory"
        test_creator = Creator(test_client)
        await test_creator.create_directory(name_to_create)
        with self.assertRaises(DirectoryAlreadyExistsError):
            await test_creator.create_directory(name_to_create)
        test_remover = Remover(test_client)
        await test_remover.remove_file(name_to_create)