import argparse
from .ftp_client import run_client 

class CommandLine:
    def __init__(self, args):
        self.args = args

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

            # Call the run_client function, passing the provided credentials
            run_client(parsed_args.username, parsed_args.password)
        else:
            parser.print_help()
