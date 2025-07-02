# Create virtual environment and switch to it
```python -m venv venv```

# Install requirements
```pip install -r requirements.txt```

# Run server with
```python run_server.py```
(on another terminal. local until we figure out a solution.)

# Command Line arguments to be considered
```
-h, --help  help me
-g, --get <file>  get file from server
-p, --put <file>  put file to server
-d, --dir  see files on server
-r, --rm  <file>  remove file on server
-c, --copy <dest> <src>  copy file to file on server
-m, --move <dest> <src>  move file to another file on server
--chmod <mode> <file>  change permissions on file on server
```

