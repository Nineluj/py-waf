from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

class RateLimiter(object):
    """Rate limiting"""
    def __init__(self, app):
        self.app = app
        self.enabled = app.config['modules'].pop('rate_limiter', True)

    def __call__(self):
        if self.enabled:
            Limiter(
                self.app,
                key_func=get_remote_address,
                default_limits=["5000/day", "500/hour"]
            )
        else:
            """Do nothing"""
            pass
