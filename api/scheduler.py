import os, sys
import time
from apscheduler.schedulers.background import BackgroundScheduler
from ltr import train_lr
from model.modelmanager import ModelManager

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

class Scheduler(object):

    def __init__(self):
        sched = BackgroundScheduler()
        # sched.add_job(self.job_trainir, 'cron', id='irtrainer_scheduler', minute='41', replace_existing=True)
        sched.add_job(self.job_trainir, 'cron', id='irtrainer_scheduler', hour='1', replace_existing=True)
        sched.add_job(self.job_trainltr, 'cron', id='ltrtrainer_scheduler', hour='3', replace_existing=True)
        # sched.add_job(self.job_trainir, 'cron', id='irtrainer_scheduler', minute='*/1', replace_existing=True)
        # sched.add_job(self.job_trainltr, 'cron', id='ltrtrainer_scheduler', minute='*/2', replace_existing=True)
        # sched.add_job(self.job_trainltr, 'interval', id='ltrtrainer_scheduler', seconds=55, replace_existing=True)
        sched.start()

        self.timeinstance = None
        self.irmodel_dic = None
        self.ltrmodel = None
        self.mm = ModelManager()

        self.job_trainir()
        self.job_trainltr()

    def job_trainir(self):
        print("job_train ir")
        self.timeinstance = time.time()
        print("timeinstance in job_trainir", self.timeinstance)
        self.irmodel_dic = self.mm.make_irmodels()
        print("job_trainir done")

    def job_trainltr(self):
        print("job_train ltr")
        cid = config.LTR_CID
        model = train_lr()
        self.ltrmodel = model
        print("job_trainltr done")

    def get_timeinstance(self):
        return self.timeinstance

    def get_irmodels(self):
        return self.irmodel_dic

    def get_ltrmodel(self):
        return self.ltrmodel

    # def start(self):
    #     self.sched.start()

