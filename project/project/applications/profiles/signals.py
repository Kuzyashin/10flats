from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, RealtyAgency
from urlshortener.models import ShortUrl
from django.utils import timezone


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=RealtyAgency)
def create_short_url(sender, instance, created, **kwargs):
    if created:
        short_url = ShortUrl.objects.create(
            basic_url='https://t.me/EmlakTech_bot?start={}'.format(str(instance.name).replace(' ', '')),
            description='ShortUrl for {}'.format(instance.name),
            pub_date=timezone.now()
        )
        short_url.save()
        instance.short_url = short_url
        instance.save()
