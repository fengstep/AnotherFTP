import aiofiles.os
from .ftp_client_exceptions import DirectoryDoesNotExistError
import os
class Remover():
    """
    Removes content from the FTP server
    """
    def __init__(self, client):
        self.client = client
    
    async def remove_file(self, file_to_remove):
        """
        Remove file from the FTP server

        file_to_remove: str
            File on the FTP server to remove
        """
        if await aiofiles.os.path.exists(os.getenv("remote_dir")+"/"+file_to_remove):
            await self.client.remove(file_to_remove)
        else:
            raise DirectoryDoesNotExistError("Can't remove file/dir, path does not exist: {}".format(file_to_remove))
        