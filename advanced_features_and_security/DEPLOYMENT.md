# Deployment Configuration for HTTPS

## SSL/TLS Certificates
SSL certificates are obtained from Let's Encrypt using Certbot.

## Nginx Configuration
Port 80 redirects all traffic to HTTPS (port 443).
SSL is configured with strong protocols and ciphers.
HSTS is enabled to enforce HTTPS.

## Django Settings
`SECURE_SSL_REDIRECT` is set to `True` to redirect HTTP to HTTPS.
HSTS settings are configured in `settings.py`.
Secure cookies are enforced for sessions and CSRF tokens.
Security headers are enabled.

## Notes

Ensure that `DEBUG` is set to `False` in production.
`ALLOWED_HOSTS` should include your domain names.