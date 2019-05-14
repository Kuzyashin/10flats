from django.db import models
from django.contrib.auth.models import User
#from messenegers.models import TelegramUser
from properites.models import Region
from urlshortener.models import ShortUrl
from django.utils.safestring import mark_safe


class Profile(models.Model):
    SUPERUSER = 'superuser'
    AGENT = 'agent'
    RENTER = 'renter'
    OWNER = 'owner'
    HOUSE_MANAGER = 'house_manager'
    UNKNOWN = 'unknown'

    _PROFILE_LEVELS = (
        (SUPERUSER, 'Superuser'),
        (AGENT, 'Agent'),
        (RENTER, 'Renter'),
        (OWNER, 'Owner'),
        (HOUSE_MANAGER, 'House manager'),
        (UNKNOWN, 'Not set'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='User'
    )
    info = models.TextField(
        max_length=500, blank=True, null=True,
        verbose_name='Info/Bio'
    )
    photo = models.ImageField(
        blank=True, null=True,
        verbose_name='Photo'
    )
    location = models.CharField(
        max_length=30, blank=True, null=True,
        verbose_name='Region'
    )
    phone = models.CharField(
        max_length=30, blank=True, null=True,
        verbose_name='Contact phone'
    )
    birth_date = models.DateField(
        null=True, blank=True,
        verbose_name='DOB'
    )
    access_level = models.CharField(
        max_length=20,
        choices=_PROFILE_LEVELS,
        verbose_name='Status',
        default=UNKNOWN
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.username + ' - ' + self.access_level


class RealtyAgency(models.Model):
    name = models.CharField(
        max_length=50, blank=True, null=True,
        verbose_name='Name'
    )
    short_url = models.ForeignKey(
        ShortUrl, models.CASCADE,
        null=True, blank=True,
        verbose_name='TG bot enter url'
    )
    phone = models.CharField(
        max_length=30, blank=True, null=True,
        verbose_name='Contact phone'
    )
    email = models.EmailField(
        blank=True, null=True,
        verbose_name='Contact email'
    )
    website = models.URLField(
        blank=True, null=True,
        verbose_name='Website'
    )
    info = models.TextField(
        blank=True, null=True,
        verbose_name='Info'
    )
    region = models.ManyToManyField(
        Region, blank=True,
        verbose_name='Region'
    )
    agents = models.ManyToManyField(
        Profile, blank=True,
        verbose_name='Agents'
    )

    class Meta:
        verbose_name = "Agency"
        verbose_name_plural = "Agencies"

    def show_qr_url(self):
        return mark_safe('<a href="%s">Open FullSize</a>' % self.short_url.qr_code)
    show_qr_url.allow_tags = True
    show_qr_url.short_description = 'QR code url'

    def show_qr_as_pic(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.short_url.qr_code)
    show_qr_as_pic.allow_tags = True
    show_qr_as_pic.short_description = 'QR code'

    def __str__(self):
        return self.name

