


class InvalidFileFormatError(Exception):
    def __init__(self, message="Invalid file data format"):
        self.message = message
        super().__init__(self.message)

class InvalidHTMLFormat(Exception):
    def __init__(self, message="Invalid HTML structure format!"):
        self.message = message
        super().__init__(self.message)


class IllegaProductState(Exception):
    def __init__(self, message="Invalid product structure!"):
        self.message = message
        super().__init__(self.message)

class InvalidMarketState(Exception):
    def __init__(self, message="Invalid market state!"):
        self.message = message
        super().__init__(self.message)
