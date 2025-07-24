import pytest
from dotenv import load_dotenv
import os
from pathlib import Path
import sys

from ..cli import CommandLine

class TestLogin():
    def test_login_with_bad_parameters(self, monkeypatch):
        try:
            os.remove(".env")
        except Exception:
            pass
        args = ["python", "-u", "user"]
        monkeypatch.setattr(sys, 'argv', args)
        myClient = CommandLine(args)
        with pytest.raises(SystemExit) as e:
            myClient.run()
        assert e.value.code == 1

    def test_login_success(self, monkeypatch):
        args = ["python", "-u", "user", "-p", "password"]
        myClient = CommandLine(args)
        monkeypatch.setattr(sys, 'argv', args)

        # 1 - Save information,
        # 2 - Do not save information (login)
        inputs = iter(["1", "quit"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(SystemExit) as e:
            myClient.run()
        
        assert os.path.exists(".env") == True # Assert we save credentials correctly
        assert e.value.code == 0 # Assert we log in and log out correctly

    def test_autologin(self, monkeypatch):
        args = ["python"]
        inputs = iter(["1", "quit"])

        print("***Autologin will fail if .env does not exist- dependent on test before.***")
        monkeypatch.setattr(sys, 'argv', args)
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        myClient = CommandLine(args)
        assert os.path.exists(".env")
        with pytest.raises(SystemExit) as e:
            myClient.run()
        assert e.value.code == 0 # Assert autologin and out correctly

        # Cleanup .env after tests
        try:
            os.remove(".env")
        except Exception:
            pass

        
