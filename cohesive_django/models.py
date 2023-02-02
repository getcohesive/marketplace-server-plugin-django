from django.db import models
import cohesive_django


class UsageTracker(models.Model):
    workspace_id = models.IntegerField(blank=False, null=False)
    instance_id = models.IntegerField(blank=False, null=False)
    used_items_count = models.IntegerField(blank=False, null=False)
    reported_items_count = models.IntegerField(blank=False, null=False)
    free_trial_items = models.IntegerField(blank=False, null=False)
    items_per_unit = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('workspace_id', 'instance_id'),)
        app_label = cohesive_django.app_label
