import os, sys
import time
import urllib.request
import json
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore,\
    register_events, register_job

from util.logmanager import logz
log = logz()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config
"""
https://zzsza.github.io/development/2018/07/07/python-scheduler/
https://yongbeomkim.github.io/django/dj-scheduler/
"""
class Scheduler:

    def __init__(self):
        log.info('start BackgroundScheduler')
        self.sched = BackgroundScheduler()
        self.sched.add_job(self.job_api_v1_init, 'cron', id=config.INIT_ID, hour=config.INIT_HOUR, replace_existing=config.INIT_REPLACE)
        self.sched.add_job(self.job_api_v1_start, 'cron', id='start', hour='5', replace_existing=True)
        self.sched.add_job(self.job_api_v1_refresh, 'cron', id='refresh', minute='*/20', replace_existing=False)
        # self.sched.add_jobstore(DjangoJobStore(), "default")
        # self.sched.start()

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        self.sched.shutdown()

    def kill_scheduler(self, job_id):
        try:
            self.sched.remove_job(job_id)
        except JobLookupError as err:
            log.info("fail to stop Scheduler: {err}".format(err=err))
            return

    def job_api_v1_init(self):
        log.info("start job_api_v1_init Scheduler")
        s = time.time()
        contents = urllib.request.urlopen("http://localhost:8800/api/v1/init?collection=ALL").read()
        rt = json.loads(contents.decode('utf-8'))
        log.info("job_api_v1_init result:%s" % rt)
        log.info("end job_api_v1_init Scheduler : %s" % (time.time()-s))

    def job_api_v1_start(self):
        log.info("start job_api_v1_start Scheduler")
        s = time.time()
        contents = urllib.request.urlopen("http://localhost:8800/api/v1/start?collection=ALL").read()
        rt = json.loads(contents.decode('utf-8'))
        log.info("job_api_v1_start result:%s" % rt)
        log.info("end job_api_v1_start Scheduler : %s" % (time.time()-s))

    def job_api_v1_refresh(self):
        log.info("start job_api_v1_refresh Scheduler")
        s = time.time()
        contents = urllib.request.urlopen("http://localhost:8800/api/v1/refresh?collection=ALL").read()
        rt = json.loads(contents.decode('utf-8'))
        log.info("job_api_v1_refresh result:%s" % rt)
        log.info("end job_api_v1_refresh Scheduler : %s" % (time.time()-s))

    def start(self):
        self.sched.start()

