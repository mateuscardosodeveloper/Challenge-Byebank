from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Resgate
from redeem.serializers import ResgateSerializer

RESGATE_URL = reverse('resgate:resgate_create')

def sample_resgate(user, **params):
    """Create and return sample resgate"""
    defaults = {
        'value': 300
    }
    defaults.update(params)

    return Resgate.objects.create(user=user, **defaults)


class PublicResgateApiTests(TestCase):
    """Test the publicly available resgate API"""

    def setUp(self):
        self.client = APIClient()

    def test_loggin_required(self):
        """Test loggin is required to access the endpoint"""
        response = self.client.get(RESGATE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateResgateApiTests(TestCase):
    """Test the private available resgate API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'test12345'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_list_resgate_to_user_authenticated(self):
        """Test retrieve list the resgate to authenticated user"""
        sample_resgate(user=self.user, value=500)
        sample_resgate(user=self.user, value=200)

        response = self.client.get(RESGATE_URL)

        resgates = Resgate.objects.all().order_by('quantity')
        serializer = ResgateSerializer(resgates, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_limited_to_user_who_made_resgate(self):
        """Test the only resgates is returned to user authenticated
        who made the resgate"""
        user2 = get_user_model().objects.create_user(
            'test2@email.com',
            'test12345'
        )
        sample_resgate(user=user2)
        sample_resgate(user=self.user)

        response = self.client.get(RESGATE_URL)

        resgates = Resgate.objects.filter(user=self.user)
        serializer = ResgateSerializer(resgates, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

    def test_new_create_resgate_successful(self):
        """Test to create a new resgate successful"""
        payload = {
            'value': 500,
            'user': self.user
        }

        response = self.client.post(RESGATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_new_create_resgate_failed(self):
        """Test to create a new resgate failed"""
        payload = {
            'value': '',
            'user': self.user
        }

        response = self.client.post(RESGATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
