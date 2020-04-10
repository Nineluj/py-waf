import requests
from hashlib import sha1

from waf.custom_types.credential_type import CredentialType
from waf.custom_types.password_strength import PasswordStrength


class Credential(object):
    def __init__(self, app):
        self.app = app
        self.enabled = (app.config['modules'].get('xss', {'enabled': True})).get('enabled', True)
        self.filtered_urls = (app.config['modules'].get('xss', {'filtered_urls': {}})).get('filtered_urls', {})
        self.password_strength = (
            app.config['modules'].get('xss', {'password_strength': PasswordStrength.VERY_UNGUESSABLE})).get(
            'password_strength', PasswordStrength.VERY_UNGUESSABLE)

    def __call__(self, uri, data):
        if not self.enabled:
            return data
        else:
            """Start checking"""
            if uri not in self.filtered_urls:
                return data
            else:
                fields = self.filtered_urls[uri]
                for arg in data:
                    if arg in fields:
                        if fields[arg] == CredentialType.EMAIL:
                            """Do something with the result here"""
                            result = self.__email_check(data[arg])
                        elif fields[arg] == CredentialType.PASSWORD:
                            """Do something with the result here"""
                            result = self.__password_check(data[arg], data)
                        else:
                            """Do nothing"""
                            pass

    def __email_check(self, email):
        """Hit the have I been pwned api for emails"""
        pass

    def __password_check(self, password):
        """Check for strength and if the password has been pwned"""
        pass

    def __is_password_pwned(self, password, data):
        """Has this password been pwned?"""
        pass

    def __is_password_unguessable(self, password, data):
        pass


class HaveIBeenPwnedApi:
    ENDPOINT = "https://api.pwnedpasswords.com/range/"

    @staticmethod
    def password_originality(password) -> int:
        """Finds the numbers of times a password has been found in a password
        leak with the HIBP API"""
        pass_hash = sha1()
        pass_hash.update(password.encode())
        pass_hex = pass_hash.hexdigest()

        pass_hex_prefix = pass_hex[:5]
        pass_hex_body = pass_hex[5:]

        # Gives us back a list of hashes whose start match the pass_hex_prefix
        resp = requests.get(f"https://api.pwnedpasswords.com/range/{pass_hex_prefix}")

        if resp.status_code != 200:
            return -1

        for line in (resp.content.decode().split("\r\n")):
            parts = line.split(":")
            if parts[0].lower() == pass_hex_body:
                return parts[1]

        return 0
