# coding=utf-8
"""
GeoHosting Controller.

.. note:: Activity
"""

from django.db import models
from django.utils import timezone

from geohosting_controller.connection import request_get
from geohosting_controller.exceptions import ConnectionErrorException


class ActivityStatus:
    """Activity Status."""

    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'


class ActivityType(models.Model):
    """Activity type contains URL."""

    identifier = models.CharField(
        unique=True,
        max_length=256,
        help_text='Activity type.'
    )
    jenkins_url = models.CharField(
        max_length=256,
        help_text='Jenkins URL.'
    )

    @property
    def url(self):
        """Return jenkins URL."""
        return self.jenkins_url

    @property
    def default_payload(self):
        """Return default payload."""
        return {
            payload.name: payload.value for payload in
            self.activitytypedefaultpayload_set.all()
        }

    def __str__(self):
        """Return activity type name."""
        return self.identifier


class ActivityTypeDefaultPayload(models.Model):
    """Activity default payload type contains URL."""

    activity_type = models.ForeignKey(
        ActivityType, on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=256,
        help_text='Name of payload.'
    )

    value = models.CharField(
        max_length=256,
        help_text='Value of payload.'
    )

    class Meta:  # noqa
        unique_together = ('activity_type', 'name')


class Activity(models.Model):
    """Activity of instance."""

    activity_type = models.ForeignKey(
        ActivityType, on_delete=models.CASCADE,
    )
    data = models.JSONField(
        null=True, blank=True
    )
    triggered_at = models.DateTimeField(
        default=timezone.now,
        editable=False
    )
    status = models.CharField(
        default=ActivityStatus.RUNNING,
        max_length=256,
        help_text='The status of activity.'
    )
    note = models.TextField(
        null=True, blank=True,
        help_text='Note about activity.'
    )

    class Meta:  # noqa
        verbose_name_plural = 'Activities'
        ordering = ('-triggered_at',)

    def run(self):
        """Run the activity."""
        try:
            response = request_get(
                url=self.activity_type.url,
                data=self.data
            )
            if response.status_code != 200:
                self.status = ActivityStatus.ERROR
                self.note = response.content
                self.save()
                raise ConnectionErrorException(
                    response.content, response=response
                )
        except Exception as e:
            self.status = ActivityStatus.ERROR
            self.note = f'{e}'
            self.save()
            raise Exception(f'{e}')

    def save(self, *args, **kwargs):
        """Override importer saved."""
        created = not self.pk
        super(Activity, self).save(*args, **kwargs)
        if created:
            self.run()
