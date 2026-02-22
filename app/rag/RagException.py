class LoaderNotFoundException(Exception):
    def __init__(self, message: str = "Loader not found for the given document type"):
        self.message = message
        super().__init__(self.message)
