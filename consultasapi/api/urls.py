from django.urls import path

from consultasapi.api import views


urlpatterns = [
    path('especialidades/', views.ListEspecialidades.as_view(), name='especialidades'),
    path('medicos/', views.ListMedicos.as_view(), name='medicos'),
    path('agendas/', views.ListAgendas.as_view(), name='agendas'),
]
