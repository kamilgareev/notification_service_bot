from django.db import models


class Notification(models.Model):
    chat_id = models.PositiveIntegerField(blank=False,
                                          null=False)
    text = models.TextField(blank=False,
                            null=False)
    time = models.DateTimeField(blank=True,
                                null=False)
    time_seconds = models.PositiveIntegerField(blank=False,
                                               null=False)
