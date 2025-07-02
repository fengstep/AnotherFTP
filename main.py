from ftp_client import CommandLine 
import sys

if __name__ == "__main__":
    myClient = CommandLine(sys.argv)
    myClient.run()