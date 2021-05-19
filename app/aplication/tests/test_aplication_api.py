from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ativo, Aplicacao
from aplication.serializers import AplicacaoSerializer


APLICACAO_URL = reverse('aplicacao:aplicacao_create')


def sample_ativos(user, **params):
    """Create and return sample ativos"""
    defaults = {
        'name': 'Investimento em Bitcoin',
    }
    defaults.update(params)

    return Ativo.objects.create(user=user, **defaults)


def sample_aplicacao(user, **params):
    """Create and return sample aplicacao"""
    defaults = {
        'value': 500,
    }
    defaults.update(params)

    return Aplicacao.objects.create(user=user, **defaults)


class PublicAplicacaoApiTests(TestCase):
    """Test the publicly available aplicação API"""

    def setUp(self):
        self.client = APIClient()

    def test_loggin_required(self):
        """Test login is required to access the endpoints"""
        response = self.client.get(APLICACAO_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAplicacaoApiTests(TestCase):
    """Test the private available aplicação API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'test12345'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_list_aplicacao(self):
        """Test to retrieve a list of aplicacao"""
        sample_aplicacao(self.user, value=200)
        sample_aplicacao(self.user, value=100)

        response = self.client.get(APLICACAO_URL)

        aplicacao = Aplicacao.objects.all().order_by('quantity')
        serializer = AplicacaoSerializer(aplicacao, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_limited_to_user_who_made_the_aplication(self):
        """Test the only aplicação is returned to user authenticated
        who made the aplication"""
        user2 = get_user_model().objects.create_user(
            'test2@email.com',
            'test12345',
        )
        sample_aplicacao(user=user2)
        sample_aplicacao(user=self.user)

        response = self.client.get(APLICACAO_URL)

        aplicacoes = Aplicacao.objects.filter(user=self.user)
        serializer = AplicacaoSerializer(aplicacoes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

    def test_create_aplicacao_to_failed(self):
        """Test to create new aplicação failed"""
        payload = {
            'value': '500',
            'ativos': '',
        }

        response = self.client.post(APLICACAO_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_aplicacao_successful(self):
        """Test to create aplicação success"""
        ativos = sample_ativos(user=self.user)
        payload = {
            'value': '500',
            'ativos': ativos.id,
        }

        response = self.client.post(APLICACAO_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)