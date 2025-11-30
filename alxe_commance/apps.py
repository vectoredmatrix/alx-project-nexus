from django.apps import AppConfig


class AlxeCommanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alxe_commance'
    
    def ready(self):
        import alxe_commance.signals
