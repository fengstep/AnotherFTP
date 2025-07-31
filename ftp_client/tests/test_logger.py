import pytest
import os
from datetime import datetime
from ..ftp_client import log_any, log_input

class TestLogger():
    def clean(self):
        try:
            os.remove("log.txt")
        except Exception as e:
            pass
        return 1
    def test_log_any(self):
        assert self.clean() == 1
        assert log_any("hello") == len("hello")
        assert os.path.exists("log.txt") == True
    def test_log_input(self, monkeypatch):
        assert self.clean() == 1
        input_str = "yes"
        with open("log.txt", "a") as log:
            log.write(f"[{datetime.now()}] CMD: {input_str}\n")
        assert os.path.exists("log.txt") == True
        with open("log.txt", "r") as file:
            for line in file:
                assert "yes" in line