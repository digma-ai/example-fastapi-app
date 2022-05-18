import django
from django.test import Client

from observability import setup_observability


class TestUsers(django.test.TransactionTestCase):

    def setUp(self):
        # Every test needs a client.
        setup_observability()
        super().setUp()

    def test_get_users_returns_an_okay_response(self):

        # Issue a GET request.
        response = self.client.get('/users/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
