import argparse
from .ftp_client import run_client
from dotenv import load_dotenv
import os

class CommandLine:
    def __init__(self, args):
        self.args = args
    def numberedAnswer(self, msg: str, choices: int) -> int:
        answer = None
        valid = False
        while not valid:
            try:
                answer = int(input(msg))
                if(answer >= 1 and answer <= choices):
                    valid = True
                else:
                    print(f"Choose an answer between 1 and {choices}.")
            except Exception:
                print("Invalid input. Try again.")
        return answer

    def run(self):
        # Create the main argument parser with a description
        parser = argparse.ArgumentParser(
            description="Simple FTP ClientCLI\n\nConnect and browse an FTP server.",
            epilog="Example usage:\n  python main.py login user1 pass123\n" 
            "MAC Example:\n  python3 main.py login user1 pass123\n",
            formatter_class=argparse.RawTextHelpFormatter)  # allows multiline epilog

        # Add a subparser group to handle different commands (e.g., login, upload, download)
        subparsers = parser.add_subparsers(dest="command", required=True)

        # Create the 'login' subcommand and define its expected arguments
        login_parser = subparsers.add_parser("login", help="Login to FTP server")
        login_parser.add_argument("username", type=str, help="Username") # First arg (required)
        login_parser.add_argument("password", type=str, help="Password") # Second arg (required)

        # Parse the command-line arguments, skipping the script name (argv[0])
        parsed_args = parser.parse_args(self.args[1:])  

        # Handles 'Login' command
        if parsed_args.command == "login":
            print(f"Client running!")
            print(f"Attempting login as {parsed_args.username}...")

            load_dotenv(".env")
            someUsername, somePassword = os.getenv("ftp_username"), os.getenv("ftp_password")
            answer = None
            # No credentials saved
            if (someUsername == None) or (somePassword == None):
                answer = self.numberedAnswer("No login credentials saved. Save now?:" \
                "\n[1] Yes\n[2] No\nAnswer: ", 2)
            # Credentials already saved
            else:
                print("Using saved credentials to login.")
                run_client(someUsername, somePassword)

            if(answer == 1): # Overwrite new saved credentials
                print("Saving credentials.")
                with open(".env", "w") as env:
                    env.write(f'username=\"{parsed_args.username}\"\npassword=\"{parsed_args.password}\"')

            # Call the run_client function, passing the provided credentials
            run_client(parsed_args.username, parsed_args.password)
        else:
            parser.print_help()
