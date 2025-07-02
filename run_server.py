import aioftp
import asyncio

async def main():
    server = aioftp.Server()
    print("aioftp Server initializing...")
    try:
        print("Server started.")
        await server.run()
    except Exception as e:
        print(f"ERROR: Server failed to start.\n{e}")

asyncio.run(main())