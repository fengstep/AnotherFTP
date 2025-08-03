import unittest
import os
import asyncio
from dotenv import load_dotenv
import aioftp
from ..ftp_client import connect_and_login, run_client_session
import threading

# Change Idle_timeout on run_server.py to 5
# Run tests with: python -m unittest ftp_client.tests.test_timeout

class TestTimeout(unittest.IsolatedAsyncioTestCase):

    async def mockServer(self):
        users = (
        aioftp.User(
                "user",
                "password",
                home_path="/remote",
                permissions = (
                aioftp.Permission("/", readable=False, writable=False),
                aioftp.Permission("/remote", readable=True, writable=True),
                )
            ),
        )
        self.server = aioftp.Server(users, idle_timeout=4)
        load_dotenv("test.env", override=True)
        print("Aioftp server initializing...")
        try:
            selectedPort = os.getenv('port')
            ip = os.getenv('ip')
            print(f"Server started at {ip}:{selectedPort}")
            await self.server.run(host=ip, port=selectedPort)

        except Exception as e:
            print(f"ERROR: Server failed to start.\n{e}")

    async def asyncSetUp(self):
        load_dotenv("test.env", override=True) # Use dev environment
        self.host = os.getenv("ip")
        self.port = int(os.getenv("port"))
        self.client = aioftp.Client()
        # Start a mock server that has timeout = 4
        asyncio.create_task(self.mockServer())
        await self.client.connect(self.host, self.port)
        await self.client.login("user", "password")

    async def asyncTearDown(self):
        try:
            await self.client.quit()
            await self.server.close()
            load_dotenv("public.env", override=True) # Refresh environment
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
        print("Waiting 6 seconds to simulate idle timeout...")
        await asyncio.sleep(6) 

        try:
        # Run a command after idle wait
            await self.client.list()
        except (ConnectionResetError, ConnectionAbortedError, aioftp.StatusCodeError) as e:
            print("Connection lost as expected due to idle timeout:", e)
        else:
            self.fail("Expected connection to be lost due to idle timeout, but command succeeded.")

