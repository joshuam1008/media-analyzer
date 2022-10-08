from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler():
    def __init__(self):
        self.background_scheduler = None

    def start_scheduler(self):
        self.background_scheduler = BackgroundScheduler()

    def stop_scheduler(self):
        self.background_scheduler.shutdown()
        self.background_scheduler = None


background_scheduler = Scheduler()
