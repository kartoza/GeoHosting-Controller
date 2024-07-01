# coding=utf-8
"""
GeoHosting Controller.

.. note:: Admins
"""
from django.contrib import admin

from geohosting_controller.models import (
    Activity, ActivityType, ActivityTypeDefaultPayload
)


class ActivityTypeDefaultPayloadInline(admin.TabularInline):
    """Inline for ActivityTypeDefaultPayload."""

    model = ActivityTypeDefaultPayload
    extra = 0


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Activity admin."""

    list_display = (
        'id', 'activity_type', 'triggered_at', 'status'
    )


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    """ActivityType admin."""

    list_display = ('identifier', 'jenkins_url')
    inlines = [ActivityTypeDefaultPayloadInline]
