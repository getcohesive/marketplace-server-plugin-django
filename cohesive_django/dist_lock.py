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
        lock = __acquire_lock(lock_key, lock_expiry_in_secs)
        if lock:
            while True:
                lock.refresh_lock()
                job_function()
                time.sleep(duration_between_jobs_in_secs)
        else:
            time.sleep(lock_retry_time_in_secs)
