from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Modalidade, Ativo

from finance.serializers import ModalidadeSerializer

MODALIDADE_URL = reverse('ativos:modalidade-list')


def detail_url(modalidade_id):
    """Return modalidade detail URL"""
    return reverse('ativos:modalidade-detail', args=[modalidade_id])


class PublicModalidadeApiTests(TestCase):
    """Test the publicly available modalide API"""

    def setUp(self):
        self.client = APIClient()

    def test_loggin_required(self):
        """Test that login is required to access the endpoints"""
        response = self.client.get(MODALIDADE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateModalidadeApiTests(TestCase):
    """Test the private modalidade API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'test12345',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_list_modalidade(self):
        """Test to retrieve a list of modalidade"""
        Modalidade.objects.create(user=self.user, name='Renda Fixa')
        Modalidade.objects.create(user=self.user, name='Renda Variável')
        Modalidade.objects.create(user=self.user, name='Cripto')

        response = self.client.get(MODALIDADE_URL)

        modalidade = Modalidade.objects.all().order_by('-name')
        serializer = ModalidadeSerializer(modalidade, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_modalidade_limieted_to_user(self):
        """Test the only modalidade for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'test2@email.com',
            'test123'
        )
        Modalidade.objects.create(user=user2, name='Renda Fixa')

        modalidade = Modalidade.objects.create(user=self.user, name='cripto')

        response = self.client.get(MODALIDADE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], modalidade.name)

    def test_create_modalidade_successful(self):
        """Test to create modalidade success"""
        payload = {'name': 'renda fixa'}
        self.client.post(MODALIDADE_URL, payload)

        exists = Modalidade.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_modalidade_failed(self):
        """Test to create modalidade when failed"""
        payload = {'name': ''}
        response = self.client.post(MODALIDADE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_modalidade(self):
        """Test to update the modalidade"""
        modalidades = Modalidade.objects.create(user=self.user, name='Cripto')
        payload = {
            'name': 'Renda Fixa'
        }

        url = detail_url(modalidades.id)
        self.client.put(url, payload)

        modalidades.refresh_from_db()
        self.assertEqual(modalidades.name, payload['name'])

    def test_retrieve_modalidades_assigned_to_ativos(self):
        """Test filtering modalidades by those assigned to ativos"""
        modalidade1 = Modalidade.objects.create(user=self.user,
                                                name='Renda Fixa')
        modalidade2 = Modalidade.objects.create(user=self.user,
                                                name='Renda Variável')
        modalidade3 = Modalidade.objects.create(user=self.user, name='Cripto')
        ativos = Ativo.objects.create(
            name='Bitcoin',
            user=self.user,
        )
        ativos.modalidades.add(modalidade3)

        response = self.client.get(MODALIDADE_URL, {'assigned_only': 1})

        serializer1 = ModalidadeSerializer(modalidade1)
        serializer2 = ModalidadeSerializer(modalidade2)
        serializer3 = ModalidadeSerializer(modalidade3)
        self.assertIn(serializer3.data, response.data)
        self.assertNotIn(serializer2.data, response.data)
        self.assertNotIn(serializer1.data, response.data)
