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
        await self.client.remove(file_to_remove)
        