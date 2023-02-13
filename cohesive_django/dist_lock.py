from .models import JobLock
import datetime
import time
from django.db import IntegrityError
# constants
SECOND = 1000
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE


def __acquire_lock(lock_key: str, lockExpiryInSeconds: int):
    try:
        print("CH_JOB_WITH_LOCK: trying to create new lock")
        lock = JobLock(job_id=lock_key, ts=datetime.datetime.utcnow().timestamp())
        lock.save()
        return lock
    except IntegrityError:
        print("CH_JOB_WITH_LOCK: failed to create new lock")
        lock = JobLock.objects.get(job_id=lock_key)
        diff = datetime.datetime.utcnow().timestamp() - lock.ts
        if diff > lockExpiryInSeconds:
            print("CH_JOB_WITH_LOCK: deleting old lock")
            lock.delete()
        else:
            print("CH_JOB_WITH_LOCK: lock is only "+str(diff)+"secs old")
        return None


def run_job_with_lock(
    lock_key: str,
    job_function,
    lock_expiry_in_secs: int = 60 * 60,
    duration_between_jobs_in_secs: int = 1,
    lock_retry_time_in_secs: int = 5 * 60,
):
    while True:
        print("CH_JOB_WITH_LOCK: checking for lock")
        lock = __acquire_lock(lock_key, lock_expiry_in_secs)
        if lock:
            print("CH_JOB_WITH_LOCK: lock acquired")
            while True:
                print("CH_JOB_WITH_LOCK: refreshing lock")
                lock.refresh_lock()
                job_function()
                print("CH_JOB_WITH_LOCK: job complete")
                time.sleep(duration_between_jobs_in_secs)
        else:
            print("CH_JOB_WITH_LOCK: lock busy. sleeping for "+str(lock_retry_time_in_secs)+ "secs")
            time.sleep(lock_retry_time_in_secs)
