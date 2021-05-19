from django.urls import path

from redeem import views

app_name = 'resgate'

urlpatterns = [
    path('', views.CreateResgateView.as_view(), name='resgate_create'),
]
