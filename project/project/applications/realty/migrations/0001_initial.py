# Generated by Django 2.2 on 2019-05-10 20:06

import core.mixins.model_mixins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('properites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RealtyComplex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=90, null=True, verbose_name='Название комплекса')),
                ('site_url', models.URLField(blank=True, null=True, verbose_name='Ссылка на комплекс')),
                ('address', models.CharField(blank=True, max_length=180, null=True, verbose_name='Полный адрес')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Фото')),
                ('google_maps_url', models.URLField(default='https://google.com', verbose_name='Ссылка на google maps')),
                ('lat', models.CharField(blank=True, max_length=10, null=True, verbose_name='Широта')),
                ('lng', models.CharField(blank=True, max_length=10, null=True, verbose_name='Долгота')),
                ('passenger_elevator', models.IntegerField(default=0, verbose_name='Количество пассажирских лифтов')),
                ('service_lift', models.IntegerField(default=0, verbose_name='Количество грузовых лифтов')),
                ('hoa', models.CharField(blank=True, max_length=50, null=True, verbose_name='ТСЖ')),
                ('year_built', models.IntegerField(blank=True, null=True, verbose_name='Год постройки')),
                ('pet_allowed', models.NullBooleanField(verbose_name='Возможно с животными')),
                ('internet', models.NullBooleanField(verbose_name='Интернет')),
                ('cctv', models.NullBooleanField(verbose_name='Видеонаблюдение')),
                ('satellite_tv', models.NullBooleanField(verbose_name='Спутниковое телевидение')),
                ('public_wifi', models.NullBooleanField(verbose_name='Wi-Fi в местах общего пользования')),
                ('floors', models.IntegerField(default=1, verbose_name='Количество Этажей')),
                ('fenced_area', models.NullBooleanField(verbose_name='Огороженная территория')),
                ('parking', models.NullBooleanField(verbose_name='Парковка')),
                ('number_of_cases', models.IntegerField(default=1, verbose_name='Количество Корпусов')),
                ('security', models.NullBooleanField(verbose_name='Наличие охраны')),
                ('intercom', models.NullBooleanField(verbose_name='Наличие домофона')),
                ('concierge', models.NullBooleanField(verbose_name='Наличие консъержа')),
                ('bbq_area', models.NullBooleanField(verbose_name='Наличие барбекю зоны')),
                ('room_service', models.NullBooleanField(verbose_name='Наличие рум-сервиса')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properites.Area', verbose_name='Район')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properites.City', verbose_name='Город')),
                ('ethnic_profile', models.ManyToManyField(blank=True, to='properites.EthnicGroup', verbose_name='Этнический профиль дома')),
                ('heating_conditioning', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properites.HeatingConditioning', verbose_name='Отопление, вентиляция и кондиционирование')),
                ('hot_water_supply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properites.HotWaterSupply', verbose_name='Горячее водоснабжение')),
                ('management_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properites.ManagementCompany', verbose_name='Управляющая компания')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properites.Region', verbose_name='Регион')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Добавил')),
                ('water_supply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properites.WaterSupply', verbose_name='Водоснабжение')),
            ],
            options={
                'verbose_name_plural': 'Жилые комплексы',
                'verbose_name': 'Жилой комплекс',
            },
        ),
        migrations.CreateModel(
            name='RealtyObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, verbose_name='Добавлено')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Фото')),
                ('site_url', models.URLField(blank=True, null=True, verbose_name='URL на сайте размещения')),
                ('rent_available', models.BooleanField(default=False, verbose_name='Возможна аренда')),
                ('flat_number', models.CharField(help_text='0 если это дом', max_length=5, verbose_name='Номер квартиры')),
                ('square', models.IntegerField(blank=True, null=True, verbose_name='Площадь')),
                ('rent_price_eur', models.IntegerField(blank=True, null=True, verbose_name='Стоимость аренды в EUR')),
                ('floor', models.IntegerField(blank=True, null=True, verbose_name='Этаж')),
                ('bathrooms', models.IntegerField(blank=True, null=True, verbose_name='Кол-во ванных комнат')),
                ('bath', models.NullBooleanField(verbose_name='Наличие ванны')),
                ('loggia', models.NullBooleanField(verbose_name='Наличие лоджии')),
                ('furnished', models.NullBooleanField(verbose_name='Мебелирована?')),
                ('appliances', models.NullBooleanField(verbose_name='Наличие бытовой техники')),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.RealtyAgency', verbose_name='Агентство')),
                ('payment_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properites.ObjectPaymentOrder', verbose_name='Порядок оплаты')),
                ('property_format', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properites.PropertyFormat', verbose_name='Формат недвижимости')),
                ('property_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properites.PropertyType', verbose_name='Тип недвижимости')),
                ('realty_complex', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='realty.RealtyComplex', verbose_name='Комплекс/Сите')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properites.InfoSource', verbose_name='Источник информации')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Добавил')),
            ],
            options={
                'verbose_name_plural': 'Объекты недвижимости',
                'verbose_name': 'Объект недвижимости',
            },
            bases=(models.Model, core.mixins.model_mixins.ModelDiffMixin),
        ),
    ]
