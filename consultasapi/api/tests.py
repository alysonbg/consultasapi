import datetime
from django.urls import reverse
from rest_framework.test import APITestCase
from consultasapi.api import models, serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class EspecialidadesViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.token = Token.objects.create(user=self.user)
        self.ortopedista = models.Especialidade.objects.create(nome='Ortopedista')
        self.cardiologista = models.Especialidade.objects.create(nome='Cardiologista')
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_return_all_especialidades(self):
        url = reverse('especialidades')

        response = self.client.get(url)
        especialidades = models.Especialidade.objects.all()
        serializer = serializers.EspecialidadeSerializer(especialidades, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_return_a_especialidade(self):
        url = reverse('especialidades') + f'?search={self.cardiologista.nome}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class MedicoViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.token = Token.objects.create(user=self.user)
        self.ortopedista = models.Especialidade.objects.create(nome='Ortopedista')
        self.cardiologista = models.Especialidade.objects.create(nome='Cardiologista')
        self.house_ortopedista = models.Medico.objects.create(nome='House', especialidade=self.ortopedista, crm='1234')
        self.house_cardiologista = models.Medico.objects.create(
            nome='House', especialidade=self.cardiologista, crm='2345'
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_return_all_medicos(self):
        url = reverse('medicos')

        response = self.client.get(url)
        medicos = models.Medico.objects.all()
        serializer = serializers.MedicoSerializer(medicos, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_filter_medico(self):
        url = reverse('medicos') + f'?search=House&especialidade=1'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class AgendaViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.token = Token.objects.create(user=self.user)
        self.ortopedista = models.Especialidade.objects.create(nome='Ortopedista')
        self.cardiologista = models.Especialidade.objects.create(nome='Cardiologista')
        self.house_ortopedista = models.Medico.objects.create(nome='House', especialidade=self.ortopedista, crm='1234')
        self.house_cardiologista = models.Medico.objects.create(
            nome='House', especialidade=self.cardiologista, crm='2345'
        )
        self.agenda = models.Agenda.objects.create(medico=self.house_cardiologista, dia=datetime.datetime.today())
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_return_all_agenda(self):
        url = reverse('agendas')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
