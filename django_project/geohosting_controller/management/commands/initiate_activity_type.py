# coding=utf-8
"""
GeoHosting Controller.

.. note:: Config App.
"""

from django.core.management.base import BaseCommand

from geohosting_controller.models import (
    ActivityType, ActivityTypeDefaultPayload
)
from geohosting_controller_client.variables import (
    ActivityType as VarActivityType,
)


class Command(BaseCommand):
    """Update all fixtures."""

    def handle(self, *args, **options):
        """Command handler."""
        for _type in VarActivityType:
            activity_type, _ = ActivityType.objects.get_or_create(
                identifier=_type.value,
                jenkins_url='https://jenkins.example.com'
            )
            if _type == VarActivityType.CREATE_INSTANCE:
                ActivityTypeDefaultPayload.objects.get_or_create(
                    activity_type=activity_type,
                    name='k8s_cluster',
                    defaults={
                        'value': 'ktz-dev-ks-gn-01'
                    }
                )
