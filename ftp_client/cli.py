import argparse
import os
import aioftp
from .ftp_client import run_client
from dotenv import load_dotenv


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
            epilog="Example usage:\n  python main.py -u USERNAME -p PASSWORD\n"
            "MAC Example:\n  python3 main.py -u USERNAME -p PASSWORD\n",
            formatter_class=argparse.RawTextHelpFormatter)  # allows multiline epilog
        
        parser.add_argument("-u", "--username", help="Username used to login to FTP", nargs=1)
        parser.add_argument("-p", "--password", help="Password used to login to FTP", nargs=1)
        args = parser.parse_args()

        load_dotenv(".env")
        savedUsername, savedPassword = os.getenv("ftp_username"), os.getenv("ftp_password")

        login_username = None
        login_password = None
        automatic_login = False

        # If no username passed, check for saved credentials.
        if(args.username == None and args.password == None):
            if(savedUsername == None or savedPassword == None):
                print("No saved credentials for login. Please supply a username and password.\nUse -h to see usage.")
                exit(1)
            else:
                automatic_login = True
                login_username = savedUsername
                login_password = savedPassword
        # Username or password passed, login as those instead
        else:
            if(args.username != None and args.password != None):
                login_username = args.username[0]
                login_password = args.password[0]
            else:
                print("Error: You must supply both username and password.")
                exit(1)
            print(f"Attempting login as {login_username}...")

        # No credentials saved, ask if they want to save
        if (savedUsername == None) or (savedPassword == None) or (savedUsername != login_username):
            answer = self.numberedAnswer("Login credentials are not saved. Save now with given arguments?:" \
            "\n[1] Yes\n[2] No\nAnswer: ", 2)
            # Overwrite new saved credentials
            if(answer == 1): 
                print("Saving credentials.")
                with open(".env", "w") as env:
                    env.write(f'ftp_username=\"{login_username}\"\nftp_password=\"{login_password}\"')
                    automatic_login = True
            else:
                print("No credentials were saved for this session.")
        else:
            print("Using saved credentials for login.")
        print(f"Client running!")
        # Call the run_client function, passing the provided credentials
        run_client(login_username, login_password, automatic_login)
