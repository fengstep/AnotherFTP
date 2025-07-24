# Create virtual environment and switch to it
```python -m venv venv```

# Install requirements
```pip install -r requirements.txt```

# Run server with
```python run_server.py```
(on another terminal. local until we figure out a solution.)

# Run tests with
```python -m unittest```

# Command Line arguments 
```
-h, --help  help me
-u <username>, --username <username> Username to login
-p <password>, --password <password> Password to login

upload <path>, Upload a file to server
download <path>, Download a file from server
remove <path>, Remove file from server
list, List files on server
local, List files locally
chmod, Change permissions on server files
quit, Logout
```

