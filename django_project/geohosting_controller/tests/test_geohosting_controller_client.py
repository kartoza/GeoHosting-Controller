# coding=utf-8
"""GeoHosting Controller."""

import os
from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test.client import Client
from django.test.testcases import TestCase
from knox.models import AuthToken
from mock import patch

from geohosting_controller_client.controller import create
from geohosting_controller_client.controller.activity import (
    get_activity_detail
)
from geohosting_controller_client.exceptions import (
    NoUrlException, NoTokenException, ConnectionErrorException
)

User = get_user_model()


def mock__request_post(url: str, data: dict, token: str):
    """Mock connection."""
    parsed_url = urlparse(url)
    url = parsed_url.path
    client = Client()
    response = client.post(
        url, data=data, headers={'Authorization': f'Token {token}'}
    )
    return response


def mock__request_get(url: str, token: str):
    """Mock connection."""
    parsed_url = urlparse(url)
    url = parsed_url.path
    client = Client()
    response = client.get(
        url, headers={'Authorization': f'Token {token}'}
    )
    return response


class ControllerTest(TestCase):
    """Test all controller functions."""

    user_email = 'test@example.com'

    def setUp(self):
        """To setup test."""
        call_command('initiate_activity_type', verbosity=0)
        self.user = User.objects.create(
            username='user', password='password'
        )
        auth_token, self.user_token = AuthToken.objects.create(
            user=self.user
        )

        self.admin = User.objects.create(
            username='admin', password='password',
            is_superuser=True,
            is_staff=True
        )
        auth_token, self.admin_token = AuthToken.objects.create(
            user=self.admin
        )

    def create_function(self):
        """Create function."""
        return create(
            'package-1', 'server.test', self.user_email
        )

    @patch(
        'geohosting_controller_client.connection._request_post',
        side_effect=mock__request_post
    )
    @patch(
        'geohosting_controller_client.connection._request_get',
        side_effect=mock__request_get
    )
    def test_create(self, request_post, request_get):
        """Test create."""
        with patch('requests.post') as mocked_requests_get:
            mocked_requests_get.return_value.status_code = 200

            # Check if no url
            with self.assertRaises(NoUrlException):
                self.create_function()
            os.environ[
                'GEOHOSTING_CONTROLLER_SERVER_URL'
            ] = 'http://server.com'

            # Check if no token
            with self.assertRaises(NoTokenException):
                self.create_function()

            # If not admin
            os.environ['GEOHOSTING_CONTROLLER_SERVER_TOKEN'] = self.user_token
            with self.assertRaises(ConnectionErrorException):
                self.create_function()

            os.environ['GEOHOSTING_CONTROLLER_SERVER_TOKEN'] = self.admin_token

            try:
                self.create_function()
                self.fail('Should have raised ConnectionErrorException')
            except ConnectionErrorException:
                pass

            try:
                os.environ['JENKINS_URL'] = 'http://jenkins.com'
                self.create_function()
                self.fail('Should have raised ConnectionErrorException')
            except ConnectionErrorException:
                pass

            # ---------------------------------------------
            # WORKING FLOW
            # ---------------------------------------------
            try:
                os.environ['JENKINS_TOKEN'] = 'Token'

                # Run create function, it will return create function
                server_activity_id = self.create_function()

                # Run webhook, should be run by Argo CD
                client = Client()
                response = client.post(
                    '/api/webhook/', data={
                        'app_name': 'server.test',
                        'state': 'successful'
                    },
                    headers={'Authorization': f'Token {self.admin_token}'}
                )
                self.assertEqual(response.status_code, 200)

                # Get the activity status from server
                activity = get_activity_detail(server_activity_id)
                status = activity['status']
                self.assertEqual(status.lower(), 'success')
                self.assertEqual(activity['data']['app_name'], 'server.test')
                self.assertEqual(activity['data']['subdomain'], 'server.test')
                self.assertEqual(activity['data']['package_id'], 'package-1')
                self.assertEqual(
                    activity['data']['user_email'], self.user_email
                )
            except ConnectionErrorException as e:
                print(f'{e}')
                self.fail("create() raised ExceptionType unexpectedly!")
