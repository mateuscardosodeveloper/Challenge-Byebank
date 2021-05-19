from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Modalidade, Ativo, Aplicacao

from finance.serializers import AtivoSerializer


ATIVOS_URL = reverse('ativos:ativo-list')


def sample_modalidade(user, name='Renda Fixa'):
    """Create and return sample modalidade"""
    return Modalidade.objects.create(user=user, name=name)


def detail_url(ativos_id):
    """Return ativo detail URL"""
    return reverse('ativos:ativo-detail', args=[ativos_id])


def sample_ativos(user, **params):
    """Create and return sample ativos"""
    defaults = {
        'name': 'Investimento em Bitcoin',
    }
    defaults.update(params)

    return Ativo.objects.create(user=user, **defaults)


class PublicAtivosApiTests(TestCase):
    """Test the publicly available ativos API"""

    def setUp(self):
        self.client = APIClient()

    def test_loggin_is_required(self):
        """Test login is required to access endpoints"""
        response = self.client.get(ATIVOS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAtivosApiTests(TestCase):
    """Test the private ativo API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'test12345'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_list_ativos(self):
        """Test to retrieve a list the ativos"""
        sample_ativos(user=self.user, name='test')
        sample_ativos(user=self.user, name='test2')

        response = self.client.get(ATIVOS_URL)

        ativos = Ativo.objects.all().order_by('id')
        serializer = AtivoSerializer(ativos, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_limited_ativos_to_user(self):
        """Test the only ativos for authenticated user is returned"""
        user2 = get_user_model().objects.create_user(
            'test2@email.com',
            'test123'
        )
        sample_ativos(user=user2, name='Investimento em Bitcoin')
        sample_ativos(user=self.user, name='Investimento imobiliário')

        response = self.client.get(ATIVOS_URL)

        ativos = Ativo.objects.filter(user=self.user)
        serializer = AtivoSerializer(ativos, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

    def test_create_ativos_successful(self):
        """Test to create ativos with success"""
        modalidades1 = sample_modalidade(user=self.user, name='blah')
        payload = {
            'name': 'investimento imobiliário',
            'modalidades': [modalidades1.id]
        }
        response = self.client.post(ATIVOS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ativos_failed(self):
        """Test to create ativos failed"""
        payload = {
            'name': 'Investimento em Bitcoin',
            'modalidades': '',
        }
        response = self.client.post(ATIVOS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_ativos(self):
        """Test to partial update the ativos"""
        ativos = sample_ativos(user=self.user)
        payload = {
            'name': 'Imobiliário'
        }

        url = detail_url(ativos.id)
        self.client.patch(url, payload)

        ativos.refresh_from_db()
        self.assertEqual(ativos.name, payload['name'])

    def test_full_update_ativos(self):
        """Test to full update the ativos"""
        ativos = sample_ativos(user=self.user)
        ativos.modalidades.add(sample_modalidade(user=self.user))
        payload = {
            'name': 'Investimento imobiliário'
        }

        url = detail_url(ativos.id)
        self.client.put(url, payload)

        ativos.refresh_from_db()
        self.assertEqual(ativos.name, payload['name'])
        modalidades = ativos.modalidades.all()
        self.assertEqual(len(modalidades), 0)

    def test_retrieve_ativos_assigned_to_aplicacao(self):
        """Test filtering ativos by those assigned to aplicacao"""
        ativos1 = sample_ativos(user=self.user, name='Bitcoin')
        ativos2 = sample_ativos(user=self.user, name='Imobiliário')
        aplicacao = Aplicacao.objects.create(
            value=500,
            user=self.user,
        )
        aplicacao.ativos.add(ativos1)

        response = self.client.get(ATIVOS_URL, {'assigned_only': 1})

        serializer1 = AtivoSerializer(ativos1)
        serializer2 = AtivoSerializer(ativos2)
        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)
