import aioftp
import asyncio
import os
from dotenv import load_dotenv
from ftp_client.uploader import Uploader

MENU = """Select an option:
    - upload
    - list
    - quit
"""

async def user_options(client):
    option = input(MENU)
    option = option.strip()
    if option.lower() == 'upload':
        dir = None
        file = None
        fpath = input('Input file or directory to upload:')
        if fpath:
            if os.path.isdir(fpath):
                dir = fpath
            else:
                file = fpath
        upload_handler = Uploader(client, path_to_file=file, path_to_dir=dir)
        await upload_handler.perform_upload()
    if option.lower() == "list":
        await list_files(client)
    return option

async def list_files(client):
    # Lists for directory and file names in remote server
    directories = []
    files = []

    # Go through and add all entries (directories & files)
    async for path, info in client.list():
        # If the type is a directory
        if info.get('type') == 'dir':
            directories.append(path.name)
        # Otherwise it's a file
        else:
            files.append(path.name)

    # List the files and directories in /server_dir on the remote server alphabetically
    if(len(directories) != 0):
        print("\nDirectories on server:")
    for d in sorted(directories):
        print(f"      {d}/")

    if(len(files) != 0):
        print("\nFiles on server:")
    for f in sorted(files):
        print(f"      {f}")
    print()


async def connect_and_login(username, password, host, port):
    client = aioftp.Client()
    try:
        print(f"Connecting to FTP remote server at {host}:{port}")
        await client.connect(host, port)

        print(f"Logging in as {username}...")
        await client.login(username, password)

        print("Login Successful!")
        
        while True:
            output = await user_options(client)
            if output.lower() == 'quit':
                await client.quit()
                print("\nConnection closed.")
                break

    except Exception as e:
        print(f"Connection/login failed: {e}")

def run_client(username, password):
    load_dotenv("public.env")
    asyncio.run(connect_and_login(username, password, os.getenv("ip"), os.getenv("port")))
