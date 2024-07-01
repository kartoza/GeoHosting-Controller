# coding=utf-8
"""
GeoHosting Controller.

.. note:: Activity.
"""

from rest_framework import serializers

from geohosting_controller.models import Activity, ActivityType


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity."""

    class Meta:  # noqa: D106
        model = Activity
        fields = '__all__'


class ActivityTypeSerializer(serializers.ModelSerializer):
    """Serializer for ActivityType."""

    class Meta:  # noqa: D106
        model = ActivityType
        fields = '__all__'
