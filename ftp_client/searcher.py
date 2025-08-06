import aioftp
import os
from .ftp_client_exceptions import ClientNoPathProvidedError

class Searcher():
    def __init__(self, client: aioftp.Client):
        self.client = client

    async def search(self, term: str) -> bool:
        result = False
        term = term.strip()
        if(len(term) < 1):
            raise(ClientNoPathProvidedError)
        async for path in self.client.list("", recursive=True):
            # print(f"Processing {str(path)}")
            if(f"{term}" in str(path)):
                print(f"Found {term} at {(str(path[0]))}")
                result = True
        return result
    
    def local_search(self, term: str) -> bool:
        term = term.strip()
        if(len(term) <= 0):
            raise ClientNoPathProvidedError
        working_directory = os.getenv("local_dir")
        result = False
        for any_path in os.listdir(working_directory):
            if term in any_path:
                print(f"Found {term} at {os.path.abspath(any_path)}")
                result = True
        return result
