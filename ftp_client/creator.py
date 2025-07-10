class Creator():
    """
    Creates content on the FTP server.
    """
    def __init__(self, client):
        self.client = client
    
    async def create_Directory(self, name):
        pass