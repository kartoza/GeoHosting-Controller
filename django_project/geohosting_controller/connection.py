# coding=utf-8
"""
GeoHosting Controller.

.. note:: Connection to the server
"""
import os

import requests
from django.conf import settings

from geohosting_controller.exceptions import NoTokenException


def _request_get(url: str, data: dict, token: str):
    """Request to server."""
    return requests.post(
        url, params=data, headers={'Authorization': f'Token {token}'}
    )


def request_get(url: str, data: dict):
    """Handle post connection."""
    try:
        token = settings.JENKINS_TOKEN
    except AttributeError:
        token = os.environ.get(
            'JENKINS_TOKEN', None
        )
    if not token:
        raise NoTokenException()

    return _request_get(url, data=data, token=token)
