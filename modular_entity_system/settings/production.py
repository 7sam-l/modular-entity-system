"""
Production settings.
Hardened security, no debug output, real email backend.
"""

from .base import *  # noqa: F401, F403

DEBUG = False

# ─── Security ──────────────────────────────────────────────────────────────────

SECURE_HSTS_SECONDS = 31_536_000          # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ─── Caching (configure your own backend in .env as needed) ────────────────────
# Example: CACHE_URL=rediscache://127.0.0.1:6379/1
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# ─── Email ─────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ─── REST Framework — production overrides ─────────────────────────────────────
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [  # noqa: F405
    'rest_framework.renderers.JSONRenderer',
    # BrowsableAPIRenderer intentionally excluded in production
]
