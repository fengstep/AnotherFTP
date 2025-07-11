import aioftp
import asyncio
from dotenv import load_dotenv
import os

async def main():
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
    server = aioftp.Server(users)
    load_dotenv("public.env")
    print("Aioftp server initializing...")
    try:
        selectedPort = os.getenv('port')
        ip = os.getenv('ip')
        print(f"Server started at {ip}:{selectedPort}")
        await server.run(host=ip, port=selectedPort)

    except Exception as e:
        print(f"ERROR: Server failed to start.\n{e}")

asyncio.run(main())