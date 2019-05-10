from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class ManagementCompany(models.Model):
    name = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Name')
    )
    site_url = models.URLField(
        null=True, blank=True,
        verbose_name=_('Site url')
    )
    phone = models.CharField(
        max_length=20,
        null=True, blank=True,
        verbose_name=_('Contact phone')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Management company")
        verbose_name_plural = _("Management companies")


class EthnicGroup(models.Model):
    name = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Group')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Ethnic Group")
        verbose_name_plural = _("Ethnic Groups")


class HeatingConditioning(models.Model):
    type = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Heating/Conditioning type')
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _("Heating/Conditioning type")
        verbose_name_plural = _("Heating/Conditioning types")


class WaterSupply(models.Model):
    type = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Water supply type')
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _("Water supply type")
        verbose_name_plural = _("Water supply types")


class HotWaterSupply(models.Model):
    type = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Water supply type')
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _("Hot water supply type")
        verbose_name_plural = _("Hot water supply type")


class PropertyType(models.Model):
    type = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Property type')
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _("Property type")
        verbose_name_plural = _("Property types")


class PropertyFormat(models.Model):
    type = models.CharField(
        max_length=10,
        null=True, blank=True,
        verbose_name=_('Property format')
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _("Property formats")
        verbose_name_plural = _("Property formats")


class ObjectPaymentOrder(models.Model):
    type = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Payment order')
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _("Payment order")
        verbose_name_plural = _("Payment orders")


class InfoSource(models.Model):
    type = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name=_('Info source')
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _("Info source")
        verbose_name_plural = _("Info sources")


class AdditionalInfo(models.Model):
    type = models.CharField(
        null=True, blank=True, max_length=40,
        verbose_name=_('Info')
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _("Additional info")
        verbose_name_plural = _("Additional info")


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

    def __str__(self):
        return self.area

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")
