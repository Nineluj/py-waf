from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


class RateLimiter(object):
    """Rate limiting"""

    def __init__(self, app):
        self.app = app
        self.enabled = (app.config['modules'].get('rate_limiter', {'enabled': True})).get('enabled', True)
        self.default_limits = (app.config['modules'].get('rate_limiter', {'default_limits': '5000/day;500/hour'})).get(
            'default_limits', '5000/day;500/hour').split(';')

    def __call__(self):
        if self.enabled:
            Limiter(
                self.app,
                key_func=get_remote_address,
                default_limits=self.default_limits
            )
        else:
            """Do nothing"""
            pass
