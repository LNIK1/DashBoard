from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone
from ckeditor.fields import RichTextField


class Category(models.Model):
    """ Категория """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name.title()


class Announcement(models.Model):
    """ Объявление """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    # text = models.CharField(max_length=255, verbose_name='Содержание')
    text = RichTextField(verbose_name='Содержание')


class Respond(models.Model):
    """ Отклик на объявление """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, verbose_name='Объявление')
    text = models.CharField(max_length=255, verbose_name='Содержание')
    respond_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки отклика')
    confirmed = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)

    def __str__(self):
        return self.text
