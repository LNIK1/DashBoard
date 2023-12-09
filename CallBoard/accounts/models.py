from django.db import models


class OneTimeCode(models.Model):
    """ Одноразовый код для подтверждения """

    user = models.CharField(max_length=255, verbose_name='Пользователь')
    code = models.CharField(max_length=6, verbose_name='Код')
