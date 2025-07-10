import aiofiles.os
from .ftp_client_exceptions import ClientFileNotFoundError, ClientNoPathProvidedError
import os
import aioftp
from dotenv import load_dotenv
class Uploader():
    def __init__(self, client: aioftp.Client, path = None):
        self.client = client
        self.path = path
    
    async def perform_upload(self):
        if(self.path): # Path exists
            if await aiofiles.os.path.exists(self.path):
                print('Uploading {}'.format(self.path))
                await self.client.upload(self.path)
                return 1
            else:
                raise ClientFileNotFoundError(self.path)
        # Path doesn't exist
        raise ClientNoPathProvidedError()
    
    async def perform_download(self):
        load_dotenv("public.env")
        if(self.path):
            if await self.client.exists(self.path):
                print('Downloading {}'.format(self.path))
                await self.client.download(self.path, os.getenv("local_dir"))
                return 1
            else:
                raise ClientFileNotFoundError(self.path)
        raise ClientNoPathProvidedError()
