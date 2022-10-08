from django.apps import AppConfig
import os


class TwitterAnalyzerConfig(AppConfig):
    """Configuration for the twitter analyzer."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'twitter_analyzer'

    def ready(self):
        # allow for the second time
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')
        if run_once is None:
            os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'
            return

        print("setting up app")
        from twitter_analyzer.scheduler import background_scheduler
        print("initialize scheduler")
        background_scheduler.start_scheduler()

        # Start stream
        from streams.twitter_stream import stream

        print("initialize stream")
        stream.toggle_module()
