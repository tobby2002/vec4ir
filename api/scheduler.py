import time
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler(object):

    def __init__(self):
        sched = BackgroundScheduler()
        sched.add_job(self.job_loadmodel, 'cron', id='model_scheduler', minute='*/1', replace_existing=True)
        sched.add_job(self.job_trainltr, 'cron', id='ltrtrainer_scheduler', hour='2', replace_existing=True)
        self.sched = sched
        self.timeinstance = None

    def job_loadmodel(self):
        self.timeinstance = time.time()
        print("timeinstance in job_loadmodel", self.timeinstance)

    def job_trainltr(self):
        print("Hello job_trainltr")

    def get_timeinstance(self):
        return self.timeinstance

    def start(self):
        self.sched.start()

