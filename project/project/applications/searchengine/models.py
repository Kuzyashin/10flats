from django.db import models
from messenegers.models import TelegramUser
from django.contrib.auth.models import User
# Create your models here.


class Search(models.Model):
    user = models.ForeignKey(
        User, models.CASCADE,
        null=True, blank=True,
        verbose_name='Аккаунт в телеграм'
    )
    telegram_user = models.ForeignKey(
        TelegramUser, models.CASCADE,
        null=True, blank=True,
        verbose_name='Аккаунт в телеграм'
    )
    progress = models.TextField(
        null=True, blank=True,
        verbose_name='Прогресс'
    )
    last_step = models.CharField(
        null=True, blank=True, max_length=20,
        verbose_name='Текущий шаг'
    )
    min_price_msg = models.CharField(
        null=True, blank=True, max_length=20,
        verbose_name='ID сообщения минимальной цены'
    )
    max_price_msg = models.CharField(
        null=True, blank=True, max_length=20,
        verbose_name='ID сообщения минимальной цены'
    )
    created_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Начало поиска'
    )
    finished_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Конец поиска'
    )
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name='Отменен?'
    )

    class Meta:
        verbose_name = "Поиск"
        verbose_name_plural = "Поиски"

    def __str__(self):
        return 'Поиск юзером' + self.telegram_user.first_name


class DistanceChoose(models.Model):
    text = models.CharField(
        null=True, blank=True, max_length=100,
        verbose_name='Текст мессенеджера'
    )
    distance = models.IntegerField(
        null=True, blank=True,
        verbose_name='Максимальное расстояние в метрах'
    )

    class Meta:
        verbose_name = "Вариант расстояния"
        verbose_name_plural = "Варианты расстояния"

    def __str__(self):
        return self.text + ' - {} м'.format(self.distance)
