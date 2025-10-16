class WrongTokenType(Exception):
    def __init__(self) -> None:
        self.message = f"Put wrong token type"
