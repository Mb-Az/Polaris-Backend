from django.db import models
from django.conf import settings
from user.models import CustomUser

class Configuration(models.Model):
    # Timing-related configs (in minutes)
    polling_interval = models.BigIntegerField(default=5)             # minutes
    measurement_interval = models.BigIntegerField(default=5)         # seconds or minutes
    server_sync_interval = models.BigIntegerField(default=15)        # minutes
    test_interval = models.BigIntegerField(default=30)               # minutes

    # URLs and phone numbers
    ping_url = models.URLField(default="https://google.com")
    web_url = models.URLField(default="https://google.com")
    sms_phone_number = models.CharField(max_length=20, default="+989107607278")

    # Feature toggles
    throughput_included = models.BooleanField(default=True)
    ping_included = models.BooleanField(default=True)
    web_included = models.BooleanField(default=True)
    dns_included = models.BooleanField(default=True)
    sms_included = models.BooleanField(default=False)

    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="updated_configs"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Configuration (Last Updated: {self.updated_at})"
