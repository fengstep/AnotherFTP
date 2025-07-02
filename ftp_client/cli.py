import argparse

class CommandLine:
    def __init__(self, args):
        # Process commands here whatever
        # Leads to other functions
        self.args = args
        pass
    def run(self):
        print("I am running!")
        for argument in self.args:
            print(f"Received argument {argument}")

