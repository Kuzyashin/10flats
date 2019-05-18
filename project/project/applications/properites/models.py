from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class EnergyClass(models.Model):
    e_class = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Energy class')
    )

    def __str__(self):
        return self.e_class

    class Meta:
        verbose_name = _("Energy class")
        verbose_name_plural = _("Energy classes")


class CustomDescription(models.Model):
    name = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Name')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Custom Description")
        verbose_name_plural = _("Custom Descriptions")


class AdditionalInfo(models.Model):
    name = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Lisainfo')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Lisainfo")
        verbose_name_plural = _("Lisainfo")


class KitchenInfo(models.Model):
    name = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Köök')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Köök")
        verbose_name_plural = _("Köök")


class WCInfo(models.Model):
    name = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Sanruum')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sanruum")
        verbose_name_plural = _("Sanruum")


class HeatingInfo(models.Model):
    name = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Küte ja ventilatsioon')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Küte ja ventilatsioon")
        verbose_name_plural = _("Küte ja ventilatsioon")


class ObjectInfo(models.Model):
    name = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Side ja turvalisus')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Side ja turvalisus")
        verbose_name_plural = _("Side ja turvalisus")


class PlaceType(models.Model):
    type = models.CharField(
        null=True, blank=True, max_length=40,
        verbose_name=_('Place type')
    )
    info = models.ManyToManyField(
        AdditionalInfo,
        verbose_name=_('Additional info')
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _("Additional info")
        verbose_name_plural = _("Additional info")


class Region(models.Model):
    region = models.CharField(
        null=True, blank=True, max_length=40,
        verbose_name=_('Region')
    )

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class City(models.Model):
    region = models.ForeignKey(
        'Region', models.CASCADE,
        null=True, blank=True,
        verbose_name=_('Region')
    )

    city = models.CharField(
        null=True, blank=True, max_length=40,
        verbose_name=_('City')
    )

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")


class Area(models.Model):
    city = models.ForeignKey(
        'City', models.CASCADE,
        null=True, blank=True,
        verbose_name=_('City')
    )

    area = models.CharField(
        null=True, blank=True, max_length=40,
        verbose_name=_('Area')
    )
    geojson = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        return self.area

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")
