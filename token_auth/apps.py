from django.apps import AppConfig


class TokenAuthConfig(AppConfig):
    name = 'token_auth'

    def ready(self):
        import token_auth.signals
