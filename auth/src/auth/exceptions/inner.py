class CredentialsAreNotProvided(Exception):
    def __init__(self, credentials_name: str) -> None:
        self.message = f"Credentials {credentials_name} are not provided"
