from flask_talisman import Talisman

"""Security headers with talisman"""


class SecurityHeaders(object):

    def __init__(self, app):
        self.app = app
        self.enabled = app.config['modules'].pop('security_headers', True)

    def __call__(self):
        """Read this from config actually. This config is quite unsafe but it is here to make the vuln-app work."""
        if self.enabled:
            Talisman(self.app, content_security_policy={
                'default-src': '\'self\'',
                'style-src': ['\'unsafe-inline\'', '\'self\''],
                'script-src': ['\'self\'', '\'unsafe-inline\'']
            })
        else:
            """Do nothing"""
            pass
