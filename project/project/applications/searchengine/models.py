from django.db import models
import uuid
#from messenegers.models import TelegramUser
from django.contrib.auth.models import User
# Create your models here.


class Search(models.Model):
    user = models.ForeignKey(
        User, models.CASCADE,
        null=True, blank=True,
        verbose_name='Аккаунт в телеграм'
    )
    hashed_id = models.UUIDField(
        default=uuid.uuid4,
        max_length=255,
        verbose_name='Уникальный идентификатор',
        unique=True,
        null=True,
        blank=True,
    )
    user_identify = models.CharField(
        null=True, blank=True, max_length=255,
        verbose_name='Идентификатор юзера'
    )
    step_1 = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 1'
    )
    step_2 = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 2'
    )
    step_3 = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 3'
    )
    step_4 = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 4'
    )
    step_4_data = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 4'
    )
    step_5 = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 5'
    )
    step_5_data = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 4'
    )
    step_6 = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 6'
    )
    step_6_data = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 4'
    )
    step_7 = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 7'
    )

    step_7_data = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 4'
    )
    step_8 = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 8'
    )
    step_8_data = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 4'
    )
    step_9 = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 9'
    )
    step_9_data = models.TextField(
        null=True, blank=True,
        verbose_name='Шаг 4'
    )
    last_step = models.IntegerField(
        null=True, blank=True,
        verbose_name='Последний шаг'
    )
    result = models.TextField(
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Начало поиска'
    )
    finished_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Конец поиска'
    )

    class Meta:
        verbose_name = "Поиск"
        verbose_name_plural = "Поиски"

"""
class TgSearch(models.Model):
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
        verbose_name = "Поиск web"
        verbose_name_plural = "Поиски web"

    def __str__(self):
        return 'Поиск юзером' + self.telegram_user.first_name
"""


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


class PercentPass(models.Model):
    percent = models.IntegerField(
        null=True, blank=True,
        verbose_name='% при котором мы учитываем результат'
    )

    class Meta:
        verbose_name = "Процент прохождения"
        verbose_name_plural = "Проценты прохождения"

    def __str__(self):
        return '{}'.format(self.percent)


class TravelType(models.Model):
    type = models.CharField(
        null=True, blank=True, max_length=80,
        verbose_name='Тип средства передвижения'
    )
    tomtom_type = models.CharField(
        null=True, blank=True, max_length=80,
        verbose_name='Тип средства передвижения для запроса в tomtom'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    class Meta:
        verbose_name = "Тип средства передвижения"
        verbose_name_plural = "Типы средства передвижения"

    def __str__(self):
        return '{}'.format(self.type)


class SearchV2(models.Model):
    user = models.ForeignKey(
        User, models.CASCADE,
        null=True, blank=True,
        verbose_name='User'
    )
    hashed_id = models.UUIDField(
        default=uuid.uuid4,
        max_length=255,
        verbose_name='Уникальный идентификатор',
        unique=True,
        null=True,
        blank=True,
    )
    user_identify = models.CharField(
        null=True, blank=True, max_length=255,
        verbose_name='Идентификатор юзера'
    )
    result = models.TextField(
        null=True, blank=True
    )
    result_full = models.TextField(
        null=True, blank=True
    )
    last_step = models.IntegerField(
        null=True, blank=True,
        verbose_name='Последний шаг'
    )
    created_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Начало поиска'
    )
    finished_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Конец поиска'
    )

    class Meta:
        verbose_name = "Поиск V2"
        verbose_name_plural = "Поиски V2"


class SearchV2step(models.Model):
    search = models.ForeignKey(
        SearchV2, models.CASCADE,
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Шаг записан'
    )
    step_pos = models.CharField(
        null=True, blank=True, max_length=80
    )
    answer = models.TextField(
        null=True, blank=True
    )
    result = models.TextField(
        null=True, blank=True
    )

    class Meta:
        verbose_name = "Шаг поиска V2"
        verbose_name_plural = "Шаги поисков V2"


class RequestViewing(models.Model):
    user = models.ForeignKey(
        User, models.CASCADE,
        null=True, blank=True
    )
    user_identify = models.CharField(
        null=True, blank=True, max_length=255,
        verbose_name='Идентификатор юзера'
    )
    search = models.ForeignKey(
        SearchV2, models.CASCADE,
        null=True, blank=True
    )
    realty_object = models.ForeignKey(
        'realty.RealtyObject', models.CASCADE,
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        null=True, blank=True
    )