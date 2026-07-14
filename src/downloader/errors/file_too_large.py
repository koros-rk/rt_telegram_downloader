class FileTooLarge(Exception):
    def __init__(self, file_size: int):
        self.file_size = file_size
        self.message = f"File size is too large: {file_size} MB"
        super().__init__(self.message)
