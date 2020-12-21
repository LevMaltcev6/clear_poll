from rest_framework.test import APITestCase
from .test_setup import TestSetUp
from ..models import User
from django.urls import reverse
from django.test import Client


class TestViews(TestSetUp):

    def create_user(self):
        from django.contrib.auth.models import User
        User.objects.create_user(
            username="string",
            password="yK8ZHyC9BrwtBi3",
            is_staff=True
        )

    @property
    def get_auth_client(self):
        res = self.client.post(reverse("token_obtain_pair"), self.user_data, format='json')
        client = Client(HTTP_AUTHORIZATION='Bearer %s' % res.data['access'])
        return client

    # Polls Admin tests
    def test_cant_add_poll_with_no_auth(self):
        res = self.client.post(reverse('poll_admin-list'))
        self.assertEqual(res.status_code, 401)

    def test_can_add_poll_with_auth_and_data(self):
        self.create_user()
        client = self.get_auth_client

        res = client.post(reverse('poll_admin-list'))
        self.assertEqual(res.status_code, 400)

    def test_polls_work_correctly(self):
        self.create_user()

        client = self.get_auth_client
        # get list
        res = client.get(reverse('poll_admin-list'))
        self.assertEqual(res.status_code, 200)
        # create
        res = client.post(reverse('poll_admin-list'), self.poll_create_dict, format='json')
        self.assertEqual(res.status_code, 201)

    def test_dont_show_list_polls_for_not_admin(self):
        res = self.client.post(reverse('poll_admin-list'))
        self.assertEqual(res.status_code, 401)


    # User tests
    def test_show_actual_polls(self):
        pass

    def test_show_questions_in_poll(self):
        pass

    def test_send_answer(self):
        pass

    def test_show_past_polls(self):
        pass









