from django.db import models

# Create your models here.


class TelegramUser(models.Model):
    first_name = models.CharField(
        null=True, blank=True, max_length=80,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        null=True, blank=True, max_length=80,
        verbose_name='Фамилия'
    )
    telegram_username = models.CharField(
        null=True, blank=True, max_length=80,
        verbose_name='Username в Telegram'
    )
    telegram_chat_id = models.IntegerField(
        null=True, blank=True,
        verbose_name='ID чата в Telegram'
    )
    telegram_phone = models.CharField(
        null=True, blank=True, max_length=20,
        verbose_name='Phone в Telegram'
    )
    referral = models.CharField(
        null=True, blank=True, max_length=20,
        verbose_name='Откуда пришел'
    )
    created_at = models.DateTimeField(
        null=False, blank=False,
        auto_created=True,
        verbose_name='Создан'
    )

    class Meta:
        verbose_name = "Аккаунт пользователя Telegram"
        verbose_name_plural = "Аккаунты пользователей Telegram"

    def __str__(self):
        return self.first_name + ' - {}'.format(self.telegram_chat_id)
