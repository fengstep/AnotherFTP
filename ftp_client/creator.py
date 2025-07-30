import aiofiles.os
from .ftp_client_exceptions import DirectoryAlreadyExistsError
import os
class Creator():
    """
    Creates content on the FTP server.
    """
    def __init__(self, client):
        self.client = client
    
    async def create_directory(self, name):
        """
        Create a directory on the FTP server.

        name: str
            Name of the directory to create
        """
        if await aiofiles.os.path.exists(os.getenv("remote_dir")+"/"+name):
            raise DirectoryAlreadyExistsError("Can't create directory, path already exists: {}".format(name))
        else:
            await self.client.make_directory(name)
