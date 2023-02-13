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
        lock = JobLock(job_id=lock_key, ts=datetime.datetime.utcnow().timestamp())
        lock.save()
        return lock
    except IntegrityError:
        lock = JobLock.objects.get(job_id=lock_key)
        if datetime.datetime.utcnow().timestamp() - lock.ts > lockExpiryInSeconds*1000:
            lock.delete()
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
