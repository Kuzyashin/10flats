from django.db import models
from django.contrib.auth.models import User
from properites.models import Region, City, Area, EnergyClass, CustomDescription, AdditionalInfo, KitchenInfo, WCInfo, HeatingInfo, ObjectInfo
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
    address = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name='Полный адрес'
    )
    google_maps_url = models.URLField(
        null=False, blank=False,
        default='https://google.com',
        verbose_name='Ссылка на google maps'
    )
    lat = models.CharField(
        max_length=20,
        null=True, blank=True,
        verbose_name='Широта'
    )
    lng = models.CharField(
        max_length=20,
        null=True, blank=True,
        verbose_name='Долгота'
    )
    year_built = models.IntegerField(
        null=True, blank=True,
        verbose_name='Год постройки'
    )
    floors = models.CharField(
        null=True, blank=True, max_length=80,
        verbose_name='Количество Этажей'
    )


    @property
    def school_dist(self):
        dist_list = DistanceMatrix.objects.filter(complex_id=self.pk, place__place_type__type='school')
        if dist_list.count() > 0:
            return dist_list.earliest('duration').distance
        else:
            return None


    @property
    def market_dist(self):
        dist_list = DistanceMatrix.objects.filter(complex_id=self.pk, place__place_type__type='supermarket')
        if dist_list.count() > 0:
            return dist_list.earliest('duration').distance
        else:
            return None


    @property
    def pharmacy_dist(self):
        dist_list = DistanceMatrix.objects.filter(complex_id=self.pk, place__place_type__type='pharmacy')
        if dist_list.count() > 0:
            return dist_list.earliest('duration').distance
        else:
            return None


    @property
    def park_dist(self):
        dist_list = DistanceMatrix.objects.filter(complex_id=self.pk, place__place_type__type='park')
        if dist_list.count() > 0:
            return dist_list.earliest('duration').distance
        else:
            return None


    @property
    def nightclub_dist(self):
        dist_list = DistanceMatrix.objects.filter(complex_id=self.pk, place__place_type__type='cafe')
        if dist_list.count() > 0:
            return dist_list.earliest('duration').distance
        else:
            return None


    @property
    def gym_dist(self):
        dist_list = DistanceMatrix.objects.filter(complex_id=self.pk, place__place_type__type='gym')
        if dist_list.count() > 0:
            return dist_list.earliest('duration').distance
        else:
            return None


    def get_nearest_supermarket(self):
        places = DistanceMatrix.objects.filter(complex_id=self.pk,
                                               place__place_type__type='supermarket').earliest('duration')
        return places.place.name + ' - ' + places.place.address + \
               ' - {}'.format(places.distance) + ' метров - {}'.format(places.duration) + ' секунд'

    def get_nearest_gym(self):
        places = DistanceMatrix.objects.filter(complex_id=self.pk,
                                               place__place_type__type='gym').earliest('duration')
        return places.place.name + ' - ' + places.place.address + \
               ' - {}'.format(places.distance) + ' метров - {}'.format(places.duration) + ' секунд'

    def get_nearest_school(self):
        places = DistanceMatrix.objects.filter(complex_id=self.pk,
                                               place__place_type__type='school').earliest('duration')
        return places.place.name + ' - ' + places.place.address + \
               ' - {}'.format(places.distance) + ' метров - {}'.format(places.duration) + ' секунд'

    def get_nearest_pharmacy(self):
        places = DistanceMatrix.objects.filter(complex_id=self.pk,
                                               place__place_type__type='pharmacy').earliest('duration')
        return places.place.name + ' - ' + places.place.address + \
               ' - {}'.format(places.distance) + ' метров - {}'.format(places.duration) + ' секунд'

    def get_nearest_park(self):
        places = DistanceMatrix.objects.filter(complex_id=self.pk,
                                               place__place_type__type='park').earliest('duration')
        return places.place.name + ' - ' + places.place.address + \
               ' - {}'.format(places.distance) + ' метров - {}'.format(places.duration) + ' секунд'

    def get_nearest_nightclub(self):
        places = DistanceMatrix.objects.filter(complex_id=self.pk,
                                               place__place_type__type='night_club').earliest('duration')
        return places.place.name + ' - ' + places.place.address + \
               ' - {}'.format(places.distance) + ' метров - {}'.format(places.duration) + ' секунд'

    def __str__(self):
        return self.address

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
    photo = models.TextField(
        null=True, blank=True,
        verbose_name='Фото'
    )

    info = models.TextField(
        null=True, blank=True
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
    site_id = models.CharField(
        null=True, blank=True, max_length=80,
        verbose_name='ID на сайте размещения',
    )
    rent_available = models.BooleanField(
        default=False,
        verbose_name='Возможна аренда'
    )
    energy_class = models.ForeignKey(
        EnergyClass, models.CASCADE,
        null=True, blank=True,
        verbose_name='Класс энергоэффективности'
    )
    custom_description = models.ManyToManyField(
        CustomDescription,
        null=True, blank=True,
        verbose_name='Кастомные поля'
    )
    additional_info = models.ManyToManyField(
        AdditionalInfo,
        null=True, blank=True,
        verbose_name='Доп инфо'
    )
    kitchen = models.ManyToManyField(
        KitchenInfo,
        null=True, blank=True,
        verbose_name='Кухня'
    )
    wc = models.ManyToManyField(
        WCInfo,
        null=True, blank=True,
        verbose_name='Туалет'
    )
    heating = models.ManyToManyField(
        HeatingInfo,
        null=True, blank=True,
        verbose_name='Отопление'
    )
    object_info = models.ManyToManyField(
        ObjectInfo,
        null=True, blank=True,
        verbose_name='инфраструктура'
    )
    rooms_count = models.IntegerField(
        null=True, blank=True,
        verbose_name='Количество комнат'
    )
    flat_number = models.CharField(
        null=False, blank=False, max_length=80,
        verbose_name='Номер квартиры',
        help_text='0 если это дом'
    )
    square = models.CharField(
        null=True, blank=True, max_length=80,
        verbose_name='Площадь'
    )
    rent_price_eur = models.IntegerField(
        null=True, blank=True,
        verbose_name='Стоимость аренды в EUR'
    )
    floor = models.IntegerField(
        null=True, blank=True,
        verbose_name='Этаж'
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
        return self.realty_complex.address

    class Meta:
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"
