from django.apps import AppConfig
from django.conf import settings

class TidbytInstallationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tidbyt_installation'

    def ready(self):
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
            scheduler.start()
