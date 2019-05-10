# Generated by Django 2.2 on 2019-05-10 21:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messenegers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('searchengine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TgSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.TextField(blank=True, null=True, verbose_name='Прогресс')),
                ('last_step', models.CharField(blank=True, max_length=20, null=True, verbose_name='Текущий шаг')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Начало поиска')),
                ('finished_at', models.DateTimeField(blank=True, null=True, verbose_name='Конец поиска')),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='Отменен?')),
                ('telegram_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='messenegers.TelegramUser', verbose_name='Аккаунт в телеграм')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Аккаунт в телеграм')),
            ],
            options={
                'verbose_name': 'Поиск web',
                'verbose_name_plural': 'Поиски web',
            },
        ),
    ]
