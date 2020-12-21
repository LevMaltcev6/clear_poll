from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from faker import Faker

class TestSetUp(APITestCase):

    def setUp(self):
        self.login_url = reverse('token_obtain_pair')

        self.user_data = {
            'username': "string",
            'password': "yK8ZHyC9BrwtBi3"
        }

        from django.utils.timezone import now
        from datetime import timedelta
        self.poll_create_dict = {
            'start_date': now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "name": "test_poll",
            'description': "test poll test poll",
            'end_date': (now()+timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:%S.%f")
        }


        return super().setUp()

    def tearDown(self):
        return super().tearDown()





