# coding=utf-8
"""GeoHosting Controller."""
from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from geohosting_controller.api.activity import (
    ActivityViewSet, ActivityTypeViewSet
)
from geohosting_controller.api.request import RequestView
from geohosting_controller.api.webhook import WebhookView

router = DefaultRouter()
router.register(
    r'activities', ActivityViewSet, basename='activities'
)

router.register(
    r'activity_types', ActivityTypeViewSet, basename='activity_types'
)

api = [
    path('request/', RequestView.as_view(), name='request-api'),
    path('webhook/', WebhookView.as_view(), name='webhook-api'),
]
api += router.urls

urlpatterns = [
    path('api/', include(api)),
    path('', RedirectView.as_view(url='/admin'), name='index')
]
