from django.apps import AppConfig


class TwitterAnalyzerConfig(AppConfig):
    """Configuration for the twitter analyzer."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'twitter_analyzer'

    def ready(self):
        print("setting up app")
        from twitter_analyzer.scheduler import background_scheduler
        background_scheduler.start_scheduler()
        # Start stream
        from streams.twitter_stream import stream
        stream.toggle_module()