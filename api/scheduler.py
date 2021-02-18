import os, sys
import time
from apscheduler.schedulers.background import BackgroundScheduler
from util.logmanager import logz
import config
log = logz()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)


class Scheduler(object):
    def __init__(self):
        sched = BackgroundScheduler()
        log.info('start BackgroundScheduler')
        # sched.add_job(self.job_trainir, 'cron', id='irtrainer_scheduler', minute='41', replace_existing=True)
        sched.add_job(self.job_trainir, 'cron', id='init_scheduler', hour='1', replace_existing=True)
        sched.add_job(self.job_trainltr, 'cron', id='ltrtrainer_scheduler', hour='3', replace_existing=True)
        # sched.add_job(self.job_trainir, 'cron', id='irtrainer_scheduler', minute='*/1', replace_existing=True)
        # sched.add_job(self.job_trainltr, 'cron', id='ltrtrainer_scheduler', minute='*/2', replace_existing=True)
        # sched.add_job(self.job_trainltr, 'interval', id='ltrtrainer_scheduler', seconds=55, replace_existing=True)
        sched.start()
        self.job_trainir()
        self.job_trainltr()

    def job_api_v1_init(self):
        pass
    def job_api_v1_start(self):
        pass
    def get_timeinstance(self):
        return self.timeinstance

    def get_irmodels(self):
        return self.irmodel_dic

    def get_ltrmodel(self):
        return self.ltrmodel

