# Generated by Django 2.2 on 2019-05-10 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('properites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='Address')),
                ('lat', models.CharField(blank=True, max_length=20, null=True, verbose_name='Lat')),
                ('lng', models.CharField(blank=True, max_length=20, null=True, verbose_name='Lng')),
                ('google_maps_url', models.URLField(blank=True, null=True, verbose_name='Google Maps url')),
                ('google_place_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='ID on Google Maps')),
                ('google_plus_code', models.CharField(blank=True, max_length=80, null=True, verbose_name='Google Plus Code on Google Maps')),
                ('place_type', models.ManyToManyField(blank=True, to='properites.PlaceType', verbose_name='Place type')),
            ],
            options={
                'verbose_name_plural': 'Places',
                'verbose_name': 'Place',
            },
        ),
    ]
