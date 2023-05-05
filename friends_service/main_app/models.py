from django.db import models


class User(models.Model):
    username = models.CharField('Название', max_length=25)

    def __str__(self):
        return self.username

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
