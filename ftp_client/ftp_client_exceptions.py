class FileNotFound(Exception):
    def __init__(self, path):
        super().__init__("Unable to find '{}'. Try using the full system path to that file/directory instead.".format(path))

class NoPathProvided(Exception):
    def __init__(self):
        super().__init__("Nothing to upload - no fpath provided.")