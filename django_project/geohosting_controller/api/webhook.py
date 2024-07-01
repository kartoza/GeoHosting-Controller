"""
GeoHosting Controller.

.. note:: Webhooks.
"""
import json

from django.http import HttpResponseBadRequest
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from geohosting_controller.models import Activity, ActivityStatus


class WebhookView(APIView):
    """Webhook receiver."""

    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        """Create new instance."""
        data = request.data
        try:
            app_name = data['app_name']
            activity = Activity.objects.filter(
                status=ActivityStatus.RUNNING
            ).filter(data__app_name=app_name).first()
            activity.status = ActivityStatus.SUCCESS
            activity.note = json.dumps(data)
            activity.save()
        except (KeyError, Activity.DoesNotExist) as e:
            return HttpResponseBadRequest(f'{e}')

        return Response()
