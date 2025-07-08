import aiofiles.os
from .ftp_client_exceptions import ClientFileNotFoundError, ClientNoFilePathError
class Uploader():
    def __init__(self, client, path_to_file=None, path_to_dir=None):
        self.path_to_chosen_file = path_to_file
        self.path_to_chosen_dir = path_to_dir
        self.client = client
    
    async def perform_upload(self):
        if self.path_to_chosen_dir:
            if await aiofiles.os.path.exists(self.path_to_chosen_dir):
                print('Uploading directory {}'.format(self.path_to_chosen_dir))
                await self.client.upload(self.path_to_chosen_dir)
            else:
                raise ClientFileNotFoundError(self.path_to_chosen_dir)
        elif self.path_to_chosen_file:
            if await aiofiles.os.path.exists(self.path_to_chosen_file):    
                print('Uploading file {}'.format(self.path_to_chosen_file))
                await self.client.upload(self.path_to_chosen_file)
            else:
                raise ClientFileNotFoundError(self.path_to_chosen_file)
        else:
            raise ClientNoFilePathError()