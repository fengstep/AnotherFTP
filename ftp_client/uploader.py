class Uploader():
    def __init__(self, path_to_file=None, path_to_dir=None):
        self.path_to_chosen_file = path_to_file
        self.path_to_chosen_dir = path_to_dir
    
    async def perform_upload(self):
        if self.path_to_chosen_dir:
            print('Uploading directory!')
        elif self.path_to_chosen_file:
            print('Uploading a single file!')
        else:
            print("No file specified.")