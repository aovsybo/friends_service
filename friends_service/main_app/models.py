from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField("username", max_length=255, unique=True)
    friends = models.ManyToManyField("self", blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='outcoming_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='incoming_requests', on_delete=models.CASCADE)
