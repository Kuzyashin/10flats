from django.db import models
from django.contrib.auth.models import User
from properites.models import ManagementCompany, EthnicGroup, HeatingConditioning,  \
    WaterSupply, HotWaterSupply, PropertyFormat, PropertyType,  \
    ObjectPaymentOrder, InfoSource, Region, City, Area
from core.models import DistanceMatrix
from django.core.exceptions import ValidationError
from core.mixins.model_mixins import ModelDiffMixin
from profiles.models import RealtyAgency


class RealtyComplex(models.Model):
    user = models.ForeignKey(
        User, models.CASCADE,
        blank=True, null=True,
        verbose_name="Добавил"
    )
    name = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name='Название комплекса'
    )
    region = models.ForeignKey(
        Region, models.CASCADE,
        null=True, blank=True,
        verbose_name='Регион'
    )
    city = models.ForeignKey(
        City, models.CASCADE,
        null=True, blank=True,
        verbose_name='Город'
    )
    area = models.ForeignKey(
        Area, models.CASCADE,
        null=True, blank=True,
        verbose_name='Район'
    )
    site_url = models.URLField(
        null=True, blank=True,
        verbose_name='Ссылка на комплекс'
    )
    address = models.CharField(
        max_length=180,
        null=True, blank=True,
        verbose_name='Полный адрес'
    )
    photo = models.ImageField(
        null=True, blank=True,
        verbose_name='Фото'
    )
    google_maps_url = models.URLField(
        null=False, blank=False,
        default='https://google.com',
        verbose_name='Ссылка на google maps'
    )
    lat = models.CharField(
        max_length=10,
        null=True, blank=True,
        verbose_name='Широта'
    )
    lng = models.CharField(
        max_length=10,
        null=True, blank=True,
        verbose_name='Долгота'
    )
    passenger_elevator = models.IntegerField(
        null=False, blank=False, default=0,
        verbose_name='Количество пассажирских лифтов'
    )
    service_lift = models.IntegerField(
        null=False, blank=False, default=0,
        verbose_name='Количество грузовых лифтов'
    )
    management_company = models.ForeignKey(
        ManagementCompany, models.CASCADE,
        null=True, blank=True,
        verbose_name='Управляющая компания'
    )
    hoa = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name='ТСЖ'
    )
    year_built = models.IntegerField(
        null=True, blank=True,
        verbose_name='Год постройки'
    )
    ethnic_profile = models.ManyToManyField(
        EthnicGroup,
        blank=True,
        verbose_name='Этнический профиль дома'
    )
    pet_allowed = models.NullBooleanField(
        verbose_name='Возможно с животными'
    )
    heating_conditioning = models.ForeignKey(
        HeatingConditioning, models.CASCADE,
        null=True, blank=True,
        verbose_name='Отопление, вентиляция и кондиционирование'
    )
    water_supply = models.ForeignKey(
        WaterSupply, models.CASCADE,
        null=True, blank=True,
        verbose_name='Водоснабжение'
    )
    hot_water_supply = models.ForeignKey(
        HotWaterSupply, models.CASCADE,
        null=True, blank=True,
        verbose_name='Горячее водоснабжение'
    )
    internet = models.NullBooleanField(
        verbose_name='Интернет'
    )
    cctv = models.NullBooleanField(
        verbose_name='Видеонаблюдение'
    )
    satellite_tv = models.NullBooleanField(
        verbose_name='Спутниковое телевидение'
    )
    public_wifi = models.NullBooleanField(
        verbose_name='Wi-Fi в местах общего пользования'
    )
    floors = models.IntegerField(
        null=False, blank=False, default=1,
        verbose_name='Количество Этажей'
    )
    fenced_area = models.NullBooleanField(
        verbose_name='Огороженная территория'
    )
    parking = models.NullBooleanField(
        verbose_name='Парковка'
    )
    number_of_cases = models.IntegerField(
        null=False, blank=False, default=1,
        verbose_name='Количество Корпусов'
    )
    security = models.NullBooleanField(
        verbose_name='Наличие охраны'
    )
    intercom = models.NullBooleanField(
        verbose_name='Наличие домофона'
    )
    concierge = models.NullBooleanField(
        verbose_name='Наличие консъержа'
    )
    bbq_area = models.NullBooleanField(
        verbose_name='Наличие барбекю зоны'
    )
    room_service = models.NullBooleanField(
        verbose_name='Наличие рум-сервиса'
    )

    @property
    def school_dist(self):
        return DistanceMatrix.objects.filter(complex__name=self.name,
                                             place__place_type__type='school').earliest('duration').distance

    @property
    def market_dist(self):
        return DistanceMatrix.objects.filter(complex__name=self.name,
                                             place__place_type__type='supermarket').earliest('duration').distance

    @property
    def pharmacy_dist(self):
        return DistanceMatrix.objects.filter(complex__name=self.name,
                                             place__place_type__type='pharmacy').earliest('duration').distance

    @property
    def park_dist(self):
        return DistanceMatrix.objects.filter(complex__name=self.name,
                                             place__place_type__type='park').earliest('duration').distance

    @property
    def nightclub_dist(self):
        return DistanceMatrix.objects.filter(complex__name=self.name,
                                             place__place_type__type='nightclub').earliest('duration').distance

    def get_nearest_supermarket(self):
        places = DistanceMatrix.objects.filter(complex__name=self.name,
                                               place__place_type__type='supermarket').earliest('duration')
        return places.place.name + ' - ' + places.place.address + \
               ' - {}'.format(places.distance) + ' метров - {}'.format(places.duration) + ' секунд'

    def get_nearest_school(self):
        places = DistanceMatrix.objects.filter(complex__name=self.name,
                                               place__place_type__type='school').earliest('duration')
        return places.place.name + ' - ' + places.place.address + \
               ' - {}'.format(places.distance) + ' метров - {}'.format(places.duration) + ' секунд'

    def get_nearest_pharmacy(self):
        places = DistanceMatrix.objects.filter(complex__name=self.name,
                                               place__place_type__type='pharmacy').earliest('duration')
        return places.place.name + ' - ' + places.place.address + \
               ' - {}'.format(places.distance) + ' метров - {}'.format(places.duration) + ' секунд'

    def get_nearest_park(self):
        places = DistanceMatrix.objects.filter(complex__name=self.name,
                                               place__place_type__type='park').earliest('duration')
        return places.place.name + ' - ' + places.place.address + \
               ' - {}'.format(places.distance) + ' метров - {}'.format(places.duration) + ' секунд'

    def get_nearest_nightclub(self):
        places = DistanceMatrix.objects.filter(complex__name=self.name,
                                               place__place_type__type='night_club').earliest('duration')
        return places.place.name + ' - ' + places.place.address + \
               ' - {}'.format(places.distance) + ' метров - {}'.format(places.duration) + ' секунд'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жилой комплекс"
        verbose_name_plural = "Жилые комплексы"


class RealtyObject(models.Model, ModelDiffMixin):
    user = models.ForeignKey(
        User, models.CASCADE,
        blank=True, null=True,
        verbose_name="Добавил"
    )
    realty_complex = models.ForeignKey(
        RealtyComplex, models.CASCADE,
        null=True, blank=True,
        verbose_name='Комплекс/Сите'
    )
    photo = models.ImageField(
        null=True, blank=True,
        verbose_name='Фото'
    )
    agency = models.ForeignKey(
        RealtyAgency, models.CASCADE,
        null=True, blank=True,
        verbose_name='Агентство'
    )
    site_url = models.URLField(
        null=True, blank=True,
        verbose_name='URL на сайте размещения'
    )
    rent_available = models.BooleanField(
        default=False,
        verbose_name='Возможна аренда'
    )
    property_type = models.ForeignKey(
        PropertyType, models.CASCADE,
        null=True, blank=True,
        verbose_name='Тип недвижимости'
    )
    property_format = models.ForeignKey(
        PropertyFormat, models.CASCADE,
        null=True, blank=True,
        verbose_name='Формат недвижимости'
    )
    flat_number = models.CharField(
        null=False, blank=False, max_length=5,
        verbose_name='Номер квартиры',
        help_text='0 если это дом'
    )
    square = models.IntegerField(
        null=True, blank=True,
        verbose_name='Площадь'
    )
    rent_price_eur = models.IntegerField(
        null=True, blank=True,
        verbose_name='Стоимость аренды в EUR'
    )
    payment_order = models.ForeignKey(
        ObjectPaymentOrder, models.CASCADE,
        null=True, blank=True,
        verbose_name='Порядок оплаты'
    )
    floor = models.IntegerField(
        null=True, blank=True,
        verbose_name='Этаж'
    )
    bathrooms = models.IntegerField(
        null=True, blank=True,
        verbose_name='Кол-во ванных комнат'
    )
    bath = models.NullBooleanField(
        verbose_name='Наличие ванны'
    )
    loggia = models.NullBooleanField(
        verbose_name='Наличие лоджии'
    )
    furnished = models.NullBooleanField(
        verbose_name='Мебелирована?'
    )
    appliances = models.NullBooleanField(
        verbose_name='Наличие бытовой техники'
    )

    source = models.ForeignKey(
        InfoSource, models.CASCADE,
        null=True, blank=True,
        verbose_name='Источник информации'
    )
    created_at = models.DateTimeField(
        auto_created=True,
        verbose_name='Добавлено'
    )

    def clean(self):

        if 'rent_available' in self.changed_fields:
            if self.rent_available and not self.rent_price_eur:
                raise ValidationError(
                    "Не установлена цена аренды")

    def __str__(self):
        return self.realty_complex.name + ' - ' + self.property_type.type \
               + ' ' + self.property_format.type

    class Meta:
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"
