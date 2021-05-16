from django.urls import path

from aplication import views
from aplication.serializers import AplicacaoSerializer


app_name = 'aplicacao'

urlpatterns = [
    path('', views.CreateAplicationView.as_view(), name='aplicacao'),
]
