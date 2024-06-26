# coding=utf-8
"""
GeoHosting Controller.

.. note:: Controller to the server
"""

from geohosting_controller_client.connection import request_post
from geohosting_controller_client.exceptions import ConnectionErrorException
from geohosting_controller_client.variables import (
    CONTROLLER_SERVER_REQUEST_URL, ActivityType
)


def create(package: str, subdomain: str, user_email: str):
    """Create an instance.

    :param package:
        The selected package that will be used to create the instance.
    :param subdomain:
        Subdomain that will be used to serve the new instance.
    :param user_email:
        user_email who trigger this activity.

    :return: Activity id from server.
    :rtype: int
    :raises ConnectionErrorException:
        If it does not return 200 from request.
        The exception object also have 'response' attribute.
    """
    app_name = subdomain
    data = {
        'request_type': ActivityType.CREATE_INSTANCE.value,
        'app_name': app_name,
        'package_id': package,
        'subdomain': subdomain,
        'user_email': user_email
    }
    response = request_post(
        url=CONTROLLER_SERVER_REQUEST_URL,
        data=data
    )
    if response.status_code != 200:
        raise ConnectionErrorException(response.content, response=response)

    return response.json()['id']
