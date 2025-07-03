import argparse
from .ftp_client import run_client

class CommandLine:
    def __init__(self, args):
        # Process commands here whatever
        # Leads to other functions
        self.args = args
        pass
    def run(self):
        print("Client running!")
        for argument in self.args:
            print(f"Received argument {argument}")
        run_client()

