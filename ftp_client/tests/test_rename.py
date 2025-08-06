import unittest
from unittest.mock import patch
import pytest
import aioftp
import os
from dotenv import load_dotenv
from ..ftp_client import local_rename, remote_rename

class TestRename(unittest.IsolatedAsyncioTestCase):
        async def asyncSetUp(self):
            load_dotenv("public.env")
            self.client = aioftp.Client()
            await self.client.connect(os.getenv("ip"), os.getenv("port"))
            await self.client.login("user", "password")
        async def asyncTearDown(self):
            await self.client.quit()

        @patch("builtins.input", side_effect=["this_is_remote.txt", "newname"])
        async def test_remote_rename_success(self, mock_input):
            assert await remote_rename(self.client) == 0 # Change to newname

        @patch("builtins.input", side_effect=["asdfjalsdfkadj", "asdjfasdlf"])
        async def test_remote_rename_no_file_found(self, mock_input):
             assert await remote_rename(self.client) == 1

        @patch("builtins.input", side_effect=["newname", "newname"])
        async def test_remote_rename_same_name(self, mock_input):
             assert await remote_rename(self.client) == 1

        @patch("builtins.input", side_effect=["", ""])
        async def test_remote_rename_no_input(self, mock_input):
             assert await remote_rename(self.client) == 1

        @patch("builtins.input", side_effect=["newname", "this_is_remote.txt"])
        async def test_remote_rename_success_2(self, mock_input):
             assert await remote_rename(self.client) == 0

###################### LOCAL

        @patch("builtins.input", side_effect=["", "this_is_local.txt", "newname"])
        async def test_local_rename_success(self, mock_input):
             assert local_rename() == 0

        @patch("builtins.input", side_effect=["", "aksdjflakdsfj", "laskdjfaldsf"])
        async def test_local_rename_no_file(self, mock_input):
             assert local_rename() == 1

        @patch("builtins.input", side_effect=["", "newname", "newname"])
        async def test_local_rename_same_name(self, mock_input):
             assert local_rename() == 1

        @patch("builtins.input", side_effect=["", "", ""])
        async def test_local_rename_no_input(self, mock_input):
             assert local_rename() == 1

        @patch("builtins.input", side_effect=["", "newname", "this_is_local.txt"])
        async def test_local_rename_success_2(self, mock_input):
             assert local_rename() == 0
        