import aioftp
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

