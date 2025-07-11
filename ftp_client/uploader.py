import aiofiles.os
from .ftp_client_exceptions import ClientFileNotFoundError, ClientNoPathProvidedError
class Uploader():
    def __init__(self, client, path = None):
        self.client = client
        self.path = path
    
    async def perform_upload(self):
        if self.path: # Path exists
            if await aiofiles.os.path.exists(self.path):
                print('Uploading {}'.format(self.path))
                await self.client.upload(self.path)
            else:
                raise ClientFileNotFoundError(self.path)
        # Path doesn't exist
        else:
            raise ClientNoPathProvidedError()
