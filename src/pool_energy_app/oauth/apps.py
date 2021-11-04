from django.apps import AppConfig


class OauthConfig(AppConfig):
    name = 'pool_energy_app.oauth'
    verbose_name = "Oauth"

    def ready(self):
        pass



    