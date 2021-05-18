from django.urls import path

from aplication import views


app_name = 'aplicacao'

urlpatterns = [
    path('', views.CreateAplicationView.as_view(), name='aplicacao'),
]
