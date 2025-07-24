import unittest
import os
import asyncio
from dotenv import load_dotenv
import aioftp
from ..ftp_client import change_remote_permissions

# run tests with: python -m unittest ftp_client.tests.test_permissions

class TestChangePermissions(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        load_dotenv("public.env")
        self.client = aioftp.Client()
        await self.client.connect(os.getenv("ip"), int(os.getenv("port")))
        await self.client.login("user", "password")

        # Create test file
        self.test_path = "test_perm_file.txt"
        with open(self.test_path, "w") as f:
            f.write("This is a test.")

        await self.client.upload(self.test_path)

    async def asyncTearDown(self):
        try:
            await self.client.remove(self.test_path)
        except Exception:
            pass
        if os.path.exists(self.test_path):
            os.remove(self.test_path)
        await self.client.quit()

    async def test_change_valid_permission(self):
        try:
            await change_remote_permissions(self.client, self.test_path, "644")
        except NotImplementedError as e:
         self.skipTest("SITE CHMOD not supported by the server.")
        except Exception as e:
            self.fail(f"Valid chmod raised an unexpected error: {e}")



    async def test_invalid_permission_mode_non_octal(self):
        with self.assertRaises(ValueError):
            await change_remote_permissions(self.client, self.test_path, "999")  # Invalid octal digits

        with self.assertRaises(ValueError):
            await change_remote_permissions(self.client, self.test_path, "abc")  # Not digits

        with self.assertRaises(ValueError):
            await change_remote_permissions(self.client, self.test_path, "77")   # Too short

    async def test_invalid_path(self):
        with self.assertRaises(ValueError):
            await change_remote_permissions(self.client, "", "644")

        with self.assertRaises(ValueError):
            await change_remote_permissions(self.client, "   ", "644")

    async def test_site_chmod_not_supported(self):
        # You can skip this if your server already shows "502 not implemented"
        # It simulates what happens if SITE CHMOD is unsupported
        # Make sure your server behaves this way or mock it
        with self.assertRaises(NotImplementedError):
            await change_remote_permissions(self.client, self.test_path, "755")
