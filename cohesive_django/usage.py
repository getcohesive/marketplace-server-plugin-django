import datetime

from cohesive import Usage, UsageParams

from cohesive_django.models import UsageTracker
from django.db.models import F


def track_usage(workspace_id: int, instance_id: int, used_items: int, free_trial_items: int, items_per_unit: int):
    try:
        usage_tracker = UsageTracker.objects.get(workspace_id=workspace_id, instance_id=instance_id)
        usage_tracker.used_items_count = F('used_items_count') + used_items
        usage_tracker.save()
    except UsageTracker.DoesNotExist:
        usage_tracker = UsageTracker(workspace_id=workspace_id, instance_id=instance_id, used_items_count=used_items, reported_items_count=0, free_trial_items=free_trial_items, items_per_unit=items_per_unit)
        usage_tracker.save()


def report_usage():
    usage_trackers = UsageTracker.objects.filter(used_items_count__gt=F('free_trial_items + reported_items_count')).get()
    for usage_tracker in usage_trackers:
        paid_usage = usage_tracker.used_items_count - usage_tracker.free_trial_items
        delta = paid_usage - usage_tracker.reported_items_count
        if delta > 0:
            # Report
            Usage.report(UsageParams(
                workspace_id=usage_tracker.workspace_id,
                instance_id=usage_tracker.instance_id,
                units=1,
                timestamp=datetime.datetime.utcnow(),
                idempotency_key=f'{(usage_tracker.reported_items_count / usage_tracker.items_per_unit) + 1}'
            ))

            # Update
            usage_tracker.reported_items_count = F('reported_items_count') + usage_tracker.items_per_unit
            usage_tracker.save()
