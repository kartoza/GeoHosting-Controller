# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from geohosting.models.support import Ticket


class TicketAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_ticket(self):
        data = {
            'customer': 'customer@example.com',
            'subject': 'Test Subject',
            'details': 'Test details',
            'status': 'open'
        }
        response = self.client.post(
            '/api/support/tickets/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().subject, 'Test Subject')

    def test_create_ticket_with_attachments(self):
        with open('path/to/test/file.txt', 'rb') as file:
            data = {
                'customer': 'customer@example.com',
                'subject': 'Test Subject',
                'details': 'Test details',
                'status': 'open',
                'attachments': file
            }
            response = self.client.post(
                '/api/support/tickets/', data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Ticket.objects.count(), 1)
            self.assertEqual(Ticket.objects.get().subject, 'Test Subject')
            self.assertEqual(Ticket.objects.get().attachments.count(), 1)
