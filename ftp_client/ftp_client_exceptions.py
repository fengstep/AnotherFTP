class ClientFileNotFoundError(Exception):
    def __init__(self, path):
        super().__init__("Unable to find '{}'. Try using the full system path to that file/directory instead.".format(path))

class ClientNoPathProvidedError(Exception):
    def __init__(self):
        super().__init__("Nothing to upload - no fpath provided.")

class DirectoryAlreadyExistsError(Exception):
    def __init__(self, path):
        super().__init__("Directory already exists: {}".format(path))

class DirectoryDoesNotExistError(Exception):
    def __init__(self, path):
        super().__init__("Directory does not exist: {}".format(path))