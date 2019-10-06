import os, sys
import time
from apscheduler.schedulers.background import BackgroundScheduler
from ltr.ltrmanager import LtrManager
from model.modelmanager import ModelManager

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

class Scheduler(object):

    def __init__(self):
        sched = BackgroundScheduler()
        sched.add_job(self.job_trainir, 'cron', id='ltrtrainer_scheduler', minute='*/1', replace_existing=True)
        sched.add_job(self.job_trainltr, 'cron', id='ltrtrainer_scheduler', minute='*/2', replace_existing=True)
        # sched.add_job(self.job_loadmodel, 'cron', id='model_scheduler', minute='*/1', replace_existing=True)
        # sched.add_job(self.job_trainltr, 'cron', id='ltrtrainer_scheduler', hour='2', replace_existing=True)
        self.sched = sched
        self.timeinstance = None

        self.irmodel_title = None
        self.irmodel_authors = None
        self.ltrmodel = None

        self.job_trainir()
        self.job_trainltr()

    def job_trainir(self):
        self.timeinstance = time.time()
        print("timeinstance in job_trainir", self.timeinstance)

        mm = ModelManager()
        w2v_title, w2v_authors = mm.make_model()
        self.irmodel_title = w2v_title
        self.irmodel_authors = w2v_authors
        print("job_trainir done")

    def job_trainltr(self):
        cid = config.LTR_CID
        ltm = LtrManager()
        model = ltm.train_dnn(cid)
        self.ltrmodel = model
        print("job_trainltr done")


    def get_timeinstance(self):
        return self.timeinstance

    def get_irmodel(self):
        return self.irmodel_title, self.irmodel_authors

    def get_ltrmodel(self):
        return self.ltrmodel

    def start(self):
        self.sched.start()

