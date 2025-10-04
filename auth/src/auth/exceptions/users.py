class UserAlreadyExists(Exception):
    def __init__(self, already_used_field: str) -> None:
        self.message = f"field {already_used_field} already use"
