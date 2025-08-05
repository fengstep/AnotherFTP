import pytest
import unittest
import aioftp
import os
from dotenv import load_dotenv

from ..searcher import Searcher
from ..ftp_client_exceptions import ClientNoPathProvidedError

class TestSearcher(unittest.IsolatedAsyncioTestCase):
    async def connect(self):
        load_dotenv("public.env")
        aio_client = aioftp.Client()
        await aio_client.connect(os.getenv("ip"), os.getenv("port"))
        await aio_client.login("user", "password")
        return aio_client
    async def test_search_not_found(self):
        client = await self.connect()
        try_search = Searcher(client)
        result = await try_search.search("KADJSFLKJSDFLJ.exe")
        assert result == False
    async def test_search_error(self):
        client = await self.connect()
        try_search = Searcher(client)
        with pytest.raises(ClientNoPathProvidedError):
            result = await try_search.search(" ")
    async def test_search_found(self):
        client = await self.connect()
        try_search = Searcher(client)
        result = await try_search.search("this_is_remote.txt")
        assert result == True
