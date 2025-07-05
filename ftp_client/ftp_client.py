import aioftp
import asyncio
from ftp_client.uploader import Uploader
MENU = """Select an option:
    - upload <path/to/file>
    - list
    - quit
"""

async def user_options(client):
    option = input(MENU)
    option = option.strip()
    if option.lower() == 'upload':
        upload_handler = Uploader(path_to_file="stufftemp.txt")
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

    # List the files and directories in ROOT DIRECTORY on the remote server alphabetically
    print("\nDirectories on server:")
    for d in sorted(directories):
        print(f"  {d}")

    print("\nFiles on server:")
    for f in sorted(files):
        print(f"  {f}")



async def connect_and_login(username, password, host="127.0.0.1", port=2121):
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
    asyncio.run(connect_and_login(username, password))
