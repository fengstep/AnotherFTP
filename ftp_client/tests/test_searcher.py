import pytest
import unittest
import aioftp
import os
from dotenv import load_dotenv

from ..searcher import Searcher
from ..ftp_client_exceptions import ClientNoPathProvidedError

class TestSearcher(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        load_dotenv("public.env")
        self.client = aioftp.Client()
        await self.client.connect(os.getenv("ip"), os.getenv("port"))
        await self.client.login("user", "password")
        self.searcher = Searcher(self.client)
    async def asyncTearDown(self):
        await self.client.quit()
    async def test_search_not_found(self):
        result = await self.searcher.search("KADJSFLKJSDFLJ.exe")
        assert result == False
    async def test_search_error(self):
        with pytest.raises(ClientNoPathProvidedError):
            result = await self.searcher.search(" ")
    async def test_search_found(self):
        result = await self.searcher.search("this_is_remote.txt")
        assert result == True
    async def test_local_search_error(self):
        with pytest.raises(ClientNoPathProvidedError):
            result = self.searcher.local_search("")
    async def test_local_search_found(self):
        result = self.searcher.local_search("this_is_local.txt")
        assert result == True
    async def test_local_search_not_found(self):
        result = self.searcher.local_search("asdfjaslkfjaslkdfjalsf.txt")
        assert result == False
