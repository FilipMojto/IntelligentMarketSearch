
class TextEditor:
    def __init__(self) -> None:
        pass

    @staticmethod
    def wrap_text(text: str, index: int = 3) -> str:
        result = ''
        for i, char in enumerate(text, start=1):
            result += char
            if i % index == 0:
                result += '\n'
        return result

    @staticmethod
    def join_text(text: str) -> str:
        result = ''

        for char in text:

            if char == '\n':
                continue

            result += char
        
        return result