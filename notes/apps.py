#notes/apps.py
from django.apps import AppConfig

class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes'
    def ready(self):
        import notes.templatetags.form_tags  # Ensure this line exists