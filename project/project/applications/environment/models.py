from django.db import models
from properites.models import PlaceType, TomTomPOI
# Create your models here.


class Place(models.Model):
    place_type = models.ManyToManyField(
        PlaceType,
        blank=True,
        verbose_name='Place type'
    )
    name = models.CharField(
        null=True, blank=True, max_length=250,
        verbose_name='Name'
    )
    address = models.CharField(
        null=True, blank=True, max_length=250,
        verbose_name='Address'
    )
    lat = models.CharField(
        null=True, blank=True, max_length=20,
        verbose_name='Lat'
    )
    lng = models.CharField(
        null=True, blank=True, max_length=20,
        verbose_name='Lng'
    )
    google_maps_url = models.URLField(
        null=True, blank=True,
        verbose_name='Google Maps url'
    )
    google_place_id = models.CharField(
        null=True, blank=True, max_length=50,
        verbose_name='ID on Google Maps'
    )
    google_plus_code = models.CharField(
        null=True, blank=True, max_length=80,
        verbose_name='Google Plus Code on Google Maps'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"


class TomTomPlace(models.Model):
    place_type = models.ManyToManyField(
        TomTomPOI,
        blank=True,
        verbose_name='Place type'
    )
    name = models.CharField(
        null=True, blank=True, max_length=250,
        verbose_name='Name'
    )
    address = models.TextField(
        null=True, blank=True,
        verbose_name='Address'
    )
    lat = models.CharField(
        null=True, blank=True, max_length=20,
        verbose_name='Lat'
    )
    lng = models.CharField(
        null=True, blank=True, max_length=20,
        verbose_name='Lng'
    )
    tomtom_place_id = models.CharField(
        null=True, blank=True, max_length=50,
        verbose_name='ID on Google Maps'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"


