"""
GeoHosting Controller.

.. note:: Config App.
"""

import copy

from django.http import HttpResponseServerError, HttpResponseBadRequest
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from geohosting_controller.models import Activity, ActivityType
from geohosting_controller_client.variables import (
    ActivityType as VarActivityType
)


class RequestView(APIView):
    """Request new instance."""

    permission_classes = (IsAuthenticated, IsAdminUser)

    def refactor_data(self, activity_type, data):
        """Refactor data."""
        # Update the data based on type
        if activity_type == VarActivityType.CREATE_INSTANCE.value:
            return {
                'subdomain': data['subdomain'],
                'user_email': data['user_email'],
                'k8s_cluster': data['k8s_cluster'],
                'geonode_size': data['package_id'],
                'geonode_name': data['app_name'],
                'package_id': data['package_id'],
                'app_name': data['app_name']
            }
        raise ActivityType.DoesNotExist()

    def post(self, request):
        """Create new instance."""
        data = copy.deepcopy(request.data)

        # Create new activity and return unique id
        try:
            request_type = data['request_type']
        except KeyError:
            return HttpResponseBadRequest(
                'request_type is required on payload.'
            )

        try:
            activity_type = ActivityType.objects.get(
                identifier__iexact=request_type
            )
            data.update(activity_type.default_payload)
            activity = Activity.objects.create(
                data=self.refactor_data(request_type, data),
                activity_type=activity_type
            )
        except ActivityType.DoesNotExist:
            return HttpResponseBadRequest(f'{request_type} does not exist.')
        except KeyError as e:
            return HttpResponseServerError(f'{e} is required')
        except Exception as e:
            return HttpResponseServerError(f'{e}')

        return Response({'id': activity.id})
