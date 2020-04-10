class CredentialException(Exception):
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return f"{self.info}"
