from django.urls import path

from consultasapi.api import views


urlpatterns = [
    path('especialidades/', views.ListEspecialidades.as_view(), name='especialidades'),
]
