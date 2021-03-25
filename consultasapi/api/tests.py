from datetime import datetime, timedelta, date
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
        url = reverse('medicos') + f'?search=House&especialidade={self.cardiologista.id}'

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
        self.agenda = models.Agenda.objects.create(medico=self.house_cardiologista, dia=datetime.today())
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_return_all_agenda(self):
        url = reverse('agendas')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class ConsultaViewDetailTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.token = Token.objects.create(user=self.user)
        self.another_user = User.objects.create_user(username='another', password='another123')
        self.token_another_user = Token.objects.create(user=self.another_user)
        self.ortopedista = models.Especialidade.objects.create(nome='Ortopedista')
        self.cardiologista = models.Especialidade.objects.create(nome='Cardiologista')
        self.house_ortopedista = models.Medico.objects.create(nome='House', especialidade=self.ortopedista, crm='1234')
        self.house_cardiologista = models.Medico.objects.create(
            nome='House', especialidade=self.cardiologista, crm='2345'
        )
        yesterday = datetime.now() - timedelta(1)
        self.agenda = models.Agenda.objects.create(medico=self.house_cardiologista, dia=yesterday)
        self.consulta = models.Consulta.objects.create(paciente=self.user, horario='14:00')

    def test_delete_consulta_from_another_user(self):
        url = reverse('consultas_detalhe', kwargs={'pk': self.consulta.id})
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_another_user.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'Error': 'Só é possível desmarcar consultas marcadas por você mesmo!'})

    def test_unable_to_delete_past_consulta(self):
        past_consulta = models.Consulta.objects.create(paciente=self.user, horario='15:00')
        self.agenda.horarios.add(past_consulta)
        url = reverse('consultas_detalhe', kwargs={'pk': past_consulta.id})
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)


class ConsultasViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.token = Token.objects.create(user=self.user)
        self.ortopedista = models.Especialidade.objects.create(nome='Ortopedista')
        self.cardiologista = models.Especialidade.objects.create(nome='Cardiologista')
        self.house_ortopedista = models.Medico.objects.create(nome='House', especialidade=self.ortopedista, crm='1234')
        self.house_cardiologista = models.Medico.objects.create(
            nome='House', especialidade=self.cardiologista, crm='2345'
        )
        yesterday = datetime.now() - timedelta(1)
        self.past_agenda = models.Agenda.objects.create(medico=self.house_cardiologista, dia=yesterday)
        self.agenda = models.Agenda.objects.create(medico=self.house_cardiologista, dia=date.today())
        self.agenda_house_ortopedista = models.Agenda.objects.create(medico=self.house_ortopedista, dia=date.today())
        self.past_consulta = models.Consulta.objects.create(paciente=self.user, horario='14:00', agenda=self.past_agenda)
        self.consulta_house_ortopedista = models.Consulta.objects.create(horario='15:00', agenda=self.agenda_house_ortopedista)
        self.consulta = models.Consulta.objects.create(paciente=self.user, horario='15:00', agenda=self.agenda)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_fail_to_create_a_consulta_using_a_past_date(self):
        url = reverse('consultas')
        data = {'agenda_id': self.past_agenda.id, 'horario': '14:00'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_fail_to_create_a_consulta_with_duplicated_time(self):
        url = reverse('consultas')
        data = {'agenda_id': self.agenda_house_ortopedista.id, 'horario': '15:00'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_fail_create_a_consulta_that_is_already_taken(self):
        another_user = User.objects.create_user(username='anotheruser', password='another123')
        another_token = Token.objects.create(user=another_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + another_token.key)
        url = reverse('consultas')
        data = {'agenda_id': self.agenda.id, 'horario': '15:00'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
