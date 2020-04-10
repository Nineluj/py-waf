import requests
from hashlib import sha1
from zxcvbn import zxcvbn

from waf.custom_types.credential_type import CredentialType
from waf.custom_types.password_strength import PasswordStrength
from waf.exceptions.credential_exception import CredentialException


class Credential(object):
    def __init__(self, app):
        self.app = app
        self.enabled = (app.config['modules'].get('xss', {'enabled': True})).get('enabled', True)
        self.filtered_urls = (app.config['modules'].get('xss', {'filtered_urls': {}})).get('filtered_urls', {})
        self.password_strength = (
            app.config['modules'].get('xss', {'password_strength': PasswordStrength.VERY_UNGUESSABLE})).get(
            'password_strength', PasswordStrength.VERY_UNGUESSABLE)
        if self.password_strength < PasswordStrength.VERY_GUESSABLE or self.password_strength > PasswordStrength.VERY_UNGUESSABLE:
            self.password_strength = PasswordStrength.VERY_UNGUESSABLE

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

    def __password_check(self, password, data):
        """Check for strength and if the password has been pwned"""
        self.__is_password_pwned(password)
        self.__is_password_unguessable(password)

    def __is_password_pwned(self, password):
        """Has this password been pwned?"""
        n_usages = HaveIBeenPwnedApi.password_originality(password)

        if n_usages == -1:
            raise CredentialException("Unable to reach HIBP API")
        elif n_usages > 500:
            raise CredentialException("Common password")
        elif n_usages > 10000:
            raise CredentialException("Very common password")

        """Do nothing"""

    def __is_password_unguessable(self, password, data):
        """Is this password easily guessable?"""
        result = zxcvbn(password, user_inputs=data)
        if result['score'] < self.password_strength:
            raise CredentialException(result['feedback'])
        else:
            """Do nothing"""
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
                return int(parts[1])

        return 0

