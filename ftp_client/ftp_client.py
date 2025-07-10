import aioftp
import asyncio
import os
from dotenv import load_dotenv
from ftp_client.uploader import Uploader

MENU = """Select an option:
    - upload
    - list
    - local
    - quit
"""

async def user_options(client):
    option = input(MENU)
    option = option.strip()
    if option.lower() == 'upload':
        fpath = input('Input file or directory to upload:')
        upload_handler = Uploader(client, fpath)
        try:
            await upload_handler.perform_upload()
        except Exception as e:
            print(f"Error with upload: {e}")
        
    elif option.lower() == "list":
        await list_files(client)

    elif option.lower() == "local":
        path = input("Enter local directory path (or press Enter for current directory): ").strip()
        if not path:
            path = "."
        list_local_directory(path)
    return option

async def list_files(client):
    # Lists for directory and file names in remote server
    load_dotenv("public.env")
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


def list_local_directory(path="."):
    """List local directories and files using os module."""
    load_dotenv("public.env")
    if(path == "."): # Auto assign localpath
        path = os.getenv("local_dir")
    try:
        # Expand ~ and get absolute path if user specified
        abs_path = os.path.abspath(os.path.expanduser(path))

        if not os.path.exists(abs_path):
            print(f"Path '{path}' does not exist.")
            return

        entries = os.listdir(abs_path)

        directories = []
        files = []

        for entry in entries:
            full_path = os.path.join(abs_path, entry)
            if os.path.isdir(full_path):
                directories.append(entry)
            else:
                files.append(entry)

        if directories:
            print("\nDirectories:")
            for d in sorted(directories):
                print(f"      {d}/")

        if files:
            print("\nFiles:")
            for f in sorted(files):
                print(f"      {f}")
        print()

    except Exception as e:
        print(f"Error reading local directory: {e}")

def run_client(username, password):
    load_dotenv("public.env")
    asyncio.run(connect_and_login(username, password,
                                  os.getenv("ip"),
                                  os.getenv("port")))
