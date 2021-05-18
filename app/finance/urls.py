from django.urls import path, include
from rest_framework.routers import DefaultRouter

from finance import views

router = DefaultRouter()
router.register('modalidade', views.ModalidadeViewSet)
router.register('ativos', views.AtivosViewSet)

app_name = 'ativos'

urlpatterns = [
    path('', include(router.urls))
]
