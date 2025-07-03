import aioftp
import asyncio

# Connect & login to remote FTP server anonymously through address
async def connect_and_login(host="127.0.0.53", port=2121):
    client = aioftp.Client()
    try:
        print(f"Connecting to FTP remote server at {host}:{port}")
        await client.connect(host, port)

        print("Anonymously logging in...")
        await client.login()

        print("Login Successful!")

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
        for dir in sorted(directories):
            print(f"    {dir}")
        
        print("\nFiles on server:")
        for file in sorted(files):
            print(f"    {file}")
        
        await client.quit()
        print("\nConnection closed.")
    except Exception as e:
        print(f"Connection/login failed: {e}")

def run_client():
    asyncio.run(connect_and_login())