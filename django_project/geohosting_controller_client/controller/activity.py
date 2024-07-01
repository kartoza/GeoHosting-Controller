# coding=utf-8
"""
GeoHosting Controller.

.. note:: Controller to the server
"""

from geohosting_controller_client.connection import request_get
from geohosting_controller_client.exceptions import ConnectionErrorException
from geohosting_controller_client.variables import (
    CONTROLLER_SERVER_REQUEST_ACTIVITY_DETAIL
)


def get_activity_detail(activity_id):
    """Fetch activity id.

    :param activity_id:
        Id of activity in the server.

    :return: Activity detail from server.
    :rtype: dict
    :raises ConnectionErrorException:
        If it does not return 200 from request.
        The exception object also have 'response' attribute.
    """
    response = request_get(
        url=CONTROLLER_SERVER_REQUEST_ACTIVITY_DETAIL.replace(
            '<id>', f'{activity_id}'
        )
    )
    if response.status_code != 200:
        raise ConnectionErrorException(response.content, response=response)

    return response.json()
