from django.contrib import admin

from core import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Modalidade)
admin.site.register(models.Ativo)
admin.site.register(models.Aplicacao)
admin.site.register(models.Resgate)
