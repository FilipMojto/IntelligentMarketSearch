
class InvalidFileFormatError(Exception):
    def __init__(self, message="Invalid file data format"):
        self.message = message
        super().__init__(self.message)