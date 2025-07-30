import unittest
import os
import asyncio
from dotenv import load_dotenv
import aioftp
from ..ftp_client import connect_and_login, run_client_session

# Change Idle_timeout on run_server.py to 5
# Run tests with: python -m unittest ftp_client.tests.test_timeout

class TestTimeout(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        load_dotenv("public.env")
        self.host = os.getenv("ip")
        self.port = int(os.getenv("port"))
        self.client = aioftp.Client()
        await self.client.connect(self.host, self.port)
        await self.client.login("user", "password")

    async def asyncTearDown(self):
        try:
            await self.client.quit()
        except Exception:
            pass

    async def test_connection_timeout(self):
        """Try to connect to a non-routable IP to trigger timeout"""
        client = aioftp.Client()
        with self.assertRaises((asyncio.TimeoutError, OSError)):
            await asyncio.wait_for(client.connect("10.255.255.1", 21), timeout=3)

    async def test_login_timeout_simulated(self):
        """Simulate a login that takes too long by subclassing aioftp.Client"""
        class SlowLoginClient(aioftp.Client):
            async def login(self, *args, **kwargs):
                await asyncio.sleep(20)  # simulate delay
                return await super().login(*args, **kwargs)

        client = SlowLoginClient()
        await client.connect(self.host, self.port)

        with self.assertRaises(asyncio.TimeoutError):
            await asyncio.wait_for(client.login("user", "password"), timeout=2)

        await client.quit()

    async def test_idle_timeout(self):
        print("Waiting 10 seconds to simulate idle timeout...")
        await asyncio.sleep(10) 

        try:
        # Run a command after idle wait
            await self.client.list()
        except (ConnectionResetError, ConnectionAbortedError, aioftp.StatusCodeError) as e:
            print("Connection lost as expected due to idle timeout:", e)
        else:
            self.fail("Expected connection to be lost due to idle timeout, but command succeeded.")

