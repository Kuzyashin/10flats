from django.db import models
from forex_python.converter import CurrencyRates
# Create your models here.


class TomTomDistanceMatrix(models.Model):
    complex = models.ForeignKey(
        'realty.RealtyComplex', models.CASCADE,
        null=True, blank=True,
        verbose_name='Realty Complex'
    )
    place = models.ForeignKey(
        'environment.TomTomPlace', models.CASCADE,
        null=True, blank=True,
        verbose_name='Place, object'
    )
    distance = models.IntegerField(
        null=True, blank=True,
        verbose_name='Distance'
    )
    duration = models.IntegerField(
        null=True, blank=True,
        verbose_name='Duration'
    )
    route = models.TextField(
        null=True, blank=True
    )
    def __str__(self):
        return self.complex.address + ' - ' + self.place.name + ' - {}'.format(self.distance)

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"


class DistanceMatrix(models.Model):
    complex = models.ForeignKey(
        'realty.RealtyComplex', models.CASCADE,
        null=True, blank=True,
        verbose_name='Realty Complex'
    )
    place = models.ForeignKey(
        'environment.Place', models.CASCADE,
        null=True, blank=True,
        verbose_name='Place, object'
    )
    distance = models.IntegerField(
        null=True, blank=True,
        verbose_name='Distance'
    )
    duration = models.IntegerField(
        null=True, blank=True,
        verbose_name='Duration'
    )

    def __str__(self):
        return self.complex.address + ' - ' + self.place.name + ' - {}'.format(self.distance)

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"


class Currency(models.Model):
    c_rates = CurrencyRates()

    code = models.CharField(
        null=True, blank=True, max_length=4,
        verbose_name='Currency code',
        help_text='You can find here : \n'
                  'https://alpari.com/ru/beginner/articles/currency-codes/'
    )
    name = models.CharField(
        null=True, blank=True, max_length=50,
        verbose_name='Name'
    )

    @property
    def to_eur_price(self):
        if self.code:
            try:
                return self.c_rates.get_rate('EUR', self.code)
            except Exception:
                return None
        else:
            return None

    def __str__(self):
        return self.code + ' - ' + self.name

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
