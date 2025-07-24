import aioftp
import asyncio
import os
import traceback
from dotenv import load_dotenv
from ftp_client.uploader import Uploader
from ftp_client.remover import Remover

MENU = """Select an option:
    - download
    - upload
    - remove
    - rename-server
    - rename-local
    - list
    - local
    - chmod
    - quit
"""

async def user_options(client):
    option = input(MENU)
    option = option.strip().lower()
    if option == 'upload':
        fpath = input('Input file or directory to upload: ')
        upload_handler = Uploader(client, fpath)
        try:
            await upload_handler.perform_upload()
        except Exception as e:
            print(f"Error with upload: {e}")   
    
    elif option == "list":
        await list_files(client)

    elif option.lower() == "remove":
        file = None
        await list_files(client)
        fpath = input("Input File/Directory to remove: ")
        remover = Remover(client)
        await remover.remove_file(fpath)
    
    elif option == "rename-server":
        return await remote_rename(client)

    elif option == "rename-local":
        return local_rename()

    elif option.lower() == "list":
        await list_files(client)

    elif option.lower() == "local":
        path = input("Enter local directory path (or press Enter for current directory): ").strip()
        if not path:
            path = "."
        list_local_directory(path)

    elif option == "download":
        await list_files(client)
        fpath = input("Enter file to download: ")
        download = Uploader(client, fpath)
        await download.perform_download()
    
    elif option.lower() == "chmod":
        path = input("Enter the remote path to file or directory: ").strip()
        mode = input("Enter the new permission mode (e.g., 755 or 644): ").strip()

        try:
            await change_remote_permissions(client, path, mode)
        except Exception as e:
            print(f"Failed to change permissions: {e}")

    return option


async def list_files(client, return_files=False):
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

    if not return_files:
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

    # Option to return file list to support other functions
    return files if return_files else None


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


async def remote_rename(client):
    # For renaming remote files on server
    # Get list of files on server from list_files function, passing it True
    files = await list_files(client, return_files=True)

    # Check if any files exist on server, return if there are none
    if not files:
        print("\nNo files on server. Nothing available to rename.\n")
        return "rename-server"

    print()
    print("Files on server:")
    for f in sorted(files):
        print(f"    {f}")
    print()

    old_name = input("Input filename to rename on server: ").strip()
    new_name = input("Input new filename: ").strip()

    # Check if user input is empty, return if either are empty
    if not old_name or not new_name:
        print("\nRename requires both the old and new filenames. Process has been stopped.\n")
        return "rename-server"

    # Check if new and old names are the same, return if they are
    if old_name == new_name:
        print("\nNew and old filenames are the same. Rename process has been stopped.\n")
        return "rename-server"

    # Check if the user provided filename actually exists on the server
    if old_name not in files:
        print(f"\n'{old_name}' not found on the server. Rename process has been stopped.\n")
        return "rename-server"

    print()
    try:
        await client.rename(old_name, new_name)
        print(f"Success! '{old_name}' has been renamed to '{new_name}' on the server.")
    except Exception as e:
        print(f"Rename on server failed: {e}")
        return "rename-server"

    # List files on server after renaming
    await list_files(client)

    return "rename-server"


def local_rename():
    # For renaming files on local machine
    path = input("Input the directory of the file to rename locally or press Enter for current directory: ").strip()
    
    if not path:
        path = os.getenv("local_dir") or "." # .env var or current dir

    # Expand to get absolute path
    absolute_path = os.path.abspath(os.path.expanduser(path))
    print(f"Absolute local path: {absolute_path}")

    # Check if dir exists, return if it doesn't
    if not os.path.isdir(absolute_path):
        print(f"\n'{absolute_path}' directory does not exist. Local rename has been stopped.\n")
        return "rename-local"
    
    list_local_directory(absolute_path)

    old_name = input("Input filename to rename locally: ").strip()
    new_name = input("Input new filename: ").strip()

    # Check if user input is empty, return if either are empty
    if not old_name or not new_name:
        print("\nRename requires both the old and new filenames. Process has been stopped.\n")
        return "rename-local"

    # Check if new and old names are the same, return if they are
    if old_name == new_name:
        print("\nNew and old filenames are the same. Rename process has been stopped.\n")
        return "rename-local"

    full_old_name = os.path.join(absolute_path, old_name)
    full_new_name = os.path.join(absolute_path, new_name)

    # Check if file actually exists, return if it doesn't
    if not os.path.exists(full_old_name):
        print(f"\n'{old_name}' does not exist in '{absolute_path}'. Rename process has been stopped.\n")
        return "rename-local"

    try:
        os.rename(full_old_name, full_new_name)
        print(f"Success! '{old_name}' has been renamed to '{new_name}' locally.")
        list_local_directory(absolute_path)
    except Exception as e:
        print(f"Local rename failed: {e}")
    print()
    return "rename-local"


async def change_remote_permissions(client, path, mode):
    # Validate permission mode
    if not mode.isdigit() or len(mode) != 3 or any(c not in "01234567" for c in mode):
        raise ValueError("Invalid permission mode. Use 3-digit octal like 755 or 644.")
    
    # Validate remote path
    if not path or not path.strip():
        raise ValueError("Invalid path. Please enter a valid remote file or directory path.")
    
    try:
        command = f"SITE CHMOD {mode} {path}"
        print(f"Sending command: {command}")
        response = await client.command(command, "2xx")
        print(f"Server response: {response.code} {response.message}")

    except aioftp.StatusCodeError as e:
        if "502" in str(e):
            raise NotImplementedError("Server does not support SITE CHMOD.")
        else:
            raise

    except Exception as e:
         raise RuntimeError(f"Unexpected error during CHMOD: {e}")


def run_client(username, password, automatic_login = False):

    load_dotenv("public.env")
    try:
        asyncio.run(connect_and_login(username, password,
                                    os.getenv("ip"),
                                    os.getenv("port")))
    except Exception as error:
        if("530" in str(error)):
            print("Credential login failed.")
            if(automatic_login == True):
                print("Saved credential login detected. They may be incorrect- deleting them now.")
                os.remove(".env")
            exit(1)
        else:
            print(f"Something went wrong with the session.\nError: {error}")
            traceback.print_exc()


async def connect_and_login(username, password, host, port):
    client = aioftp.Client()
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
            exit(0) 