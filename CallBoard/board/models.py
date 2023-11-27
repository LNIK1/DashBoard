from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone
import ckeditor


class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name.title()


class Announcement(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.CharField(max_length=255, verbose_name='Содержание')


class Respond(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, verbose_name='Объявление')
    text = models.CharField(max_length=255, verbose_name='Содержание')
