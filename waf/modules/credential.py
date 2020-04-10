from http import HTTPStatus

import requests
from hashlib import sha1
from zxcvbn import zxcvbn

from waf.custom_types.credential_type import CredentialType
from waf.custom_types.password_strength import PasswordStrength
from waf.exceptions.credential_exception import CredentialException


class CredentialCheck(object):
    def __init__(self, app):
        self.app = app
        self.enabled = (app.config['modules'].get('credential', {'enabled': True})).get('enabled', True)
        self.filtered_urls = (app.config['modules'].get('credential', {'filtered_urls': {}})).get('filtered_urls', {})
        self.password_strength = PasswordStrength((
            app.config['modules'].get('credential', {'password_strength': PasswordStrength.VERY_UNGUESSABLE})).get(
            'password_strength', PasswordStrength.VERY_UNGUESSABLE))
        if self.password_strength.value < PasswordStrength.VERY_GUESSABLE.value or self.password_strength.value > PasswordStrength.VERY_UNGUESSABLE.value:
            self.password_strength = PasswordStrength.VERY_UNGUESSABLE
        self.password_check_api = 'https://api.pwnedpasswords.com/range/{}'
        self.email_check_api = 'https://digibody.avast.com/v1/web/leaks'

    def __call__(self, uri, data):
        """Return True if this is matching a filtered_url"""
        if not self.enabled:
            return False
        else:
            """Start checking"""
            if uri not in self.filtered_urls:
                return False
            else:
                fields = self.filtered_urls[uri]
                for arg in data:
                    if arg in fields:
                        if CredentialType(fields[arg]) == CredentialType.EMAIL:
                            """Do something with the result here"""
                            self.__email_check(data[arg])
                        elif CredentialType(fields[arg]) == CredentialType.PASSWORD:
                            """Do something with the result here"""
                            self.__password_check(data[arg], data)
                        else:
                            """Do nothing"""
                            pass
                return True

    def __email_check(self, email):
        """Hit the have I been pwned api for emails"""
        res = requests.post(self.email_check_api, json={'email': email})
        if res.status_code != HTTPStatus.OK:
            raise CredentialException("Email check API is misbehaving")
        values = res.json().get('value', [])
        if values:
            raise CredentialException(f"Email found in {len(values)} breaches")
        pass

    def __password_check(self, password, data):
        """Check for strength and if the password has been pwned"""
        self.__is_password_pwned(password)
        self.__is_password_unguessable(password, data)

    def __is_password_pwned(self, password):
        """Has this password been pwned?"""
        password_hash = sha1(password.encode()).hexdigest()
        res = requests.get(self.password_check_api.format(password_hash[:5]))

        if res.status_code != HTTPStatus.OK:
            raise CredentialException("Unable to reach HIBP API")

        for line in (res.content.decode().split("\r\n")):
            parts = line.split(":")
            if parts[0].lower() == password_hash[5:]:
                times_found = int(parts[1])
                if times_found > 10000:
                    raise CredentialException("Very common password")
                elif times_found > 500:
                    raise CredentialException("Common password")
                elif times_found > 0:
                    raise CredentialException("Breached password")

    def __is_password_unguessable(self, password, data):
        """Is this password easily guessable?"""
        result = zxcvbn(password, user_inputs=data)
        if result['score'] < self.password_strength.value:
            raise CredentialException(result['feedback'])
        else:
            """Do nothing"""
            pass
