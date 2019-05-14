from django.core.management.base import BaseCommand
from realty.models import RealtyComplex, RealtyObject
from properites.models import Region, City, Area, EnergyClass, CustomDescription,\
    AdditionalInfo, KitchenInfo, WCInfo, HeatingInfo, ObjectInfo
from django.contrib.auth.models import User
from profiles.models import RealtyAgency, Profile
from django.utils import timezone
import requests
from django.db.utils import IntegrityError


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        url = 'https://www.kv.ee/?act=search.agentobjectsy&api_key=cPX86TTn&agent_id=563653&start=0&limit=10000&include_ads=1'
        data = requests.get(url)
        counto = len(data.json())
        iii=1
        for realty_object in data.json():
            print('{} / {}'.format(iii, counto))
            try:
                region = Region.objects.get(region=realty_object['address_county'])
            except Region.DoesNotExist:
                region = Region.objects.create(
                    region=realty_object['address_county']
                )
            try:
                city = City.objects.get(city=realty_object['address_parish'])
            except City.DoesNotExist:
                city = City.objects.create(
                    region=region,
                    city=realty_object['address_parish']
                )
            try:
                area = Area.objects.get(area=realty_object['address_city'])
            except Area.DoesNotExist:
                area = Area.objects.create(
                    city=city,
                    area=realty_object['address_city']
                )
            try:
                realty_obj = RealtyObject.objects.get(site_id=realty_object['object_id'])
            except RealtyObject.DoesNotExist:
                try:
                    complex = RealtyComplex.objects.get(address='{} {} {}'.format(
                        realty_object['address_city'],
                        realty_object['address_street'],
                        realty_object['address_house']
                    ))
                except RealtyComplex.DoesNotExist:
                    complex = RealtyComplex.objects.create(
                        address='{} {} {}'.format(
                            realty_object['address_city'],
                            realty_object['address_street'],
                            realty_object['address_house']
                        ),
                        city=city,
                        region=region,
                        area=area,
                        lat=str(realty_object['coordinates']).split(',')[0] if realty_object['coordinates'] else None,
                        lng=str(realty_object['coordinates']).split(',')[1] if realty_object['coordinates'] else None,
                        floors=realty_object['num_floors']
                    )
                realty_obj = RealtyObject.objects.create(
                    realty_complex=complex,
                    photo=realty_object['images_big'],
                    info=realty_object['description'],
                    site_url=realty_object['static_url'],
                    site_id=realty_object['object_id'],
                    rent_available=True,
                    rooms_count=realty_object['room_count'],
                    square=realty_object['area_total'],
                    rent_price_eur=realty_object['price'],
                    floor=realty_object['this_floor'],
                    created_at=timezone.now()
                )
                for desc_data in realty_object['short_description']:
                    if desc_data.get('title') == '':
                        for param in desc_data.get('params'):
                            try:
                                add_info = CustomDescription.objects.get(name=param)
                            except CustomDescription.DoesNotExist:
                                add_info = CustomDescription.objects.create(name=param)
                            realty_obj.custom_description.add(add_info)
                    elif desc_data.get('title') == 'Lisainfo':
                        for param in desc_data.get('params'):
                            try:
                                add_info = AdditionalInfo.objects.get(name=param)
                            except AdditionalInfo.DoesNotExist:
                                add_info = AdditionalInfo.objects.create(name=param)
                            realty_obj.additional_info.add(add_info)
                    elif desc_data.get('title') == 'Köök':
                        for param in desc_data.get('params'):
                            try:
                                add_info = KitchenInfo.objects.get(name=param)
                            except KitchenInfo.DoesNotExist:
                                add_info = KitchenInfo.objects.create(name=param)
                            realty_obj.kitchen.add(add_info)
                    elif desc_data.get('title') == 'Sanruum':
                        for param in desc_data.get('params'):
                            try:
                                add_info = WCInfo.objects.get(name=param)
                            except WCInfo.DoesNotExist:
                                add_info = WCInfo.objects.create(name=param)
                            realty_obj.wc.add(add_info)
                    elif desc_data.get('title') == 'Küte ja ventilatsioon':
                        for param in desc_data.get('params'):
                            try:
                                add_info = HeatingInfo.objects.get(name=param)
                            except HeatingInfo.DoesNotExist:
                                add_info = HeatingInfo.objects.create(name=param)
                            realty_obj.heating.add(add_info)
                    elif desc_data.get('title') == 'Side ja turvalisus':
                        for param in desc_data.get('params'):
                            try:
                                add_info = ObjectInfo.objects.get(name=param)
                            except ObjectInfo.DoesNotExist:
                                add_info = ObjectInfo.objects.create(name=param)
                            realty_obj.object_info.add(add_info)
            try:
                agency = RealtyAgency.objects.get(name=realty_object['broker'].get('company_name'))
            except RealtyAgency.DoesNotExist:
                agency = RealtyAgency.objects.create(
                    name=realty_object['broker'].get('company_name'),
                )
            try:
                user = User.objects.get(email=realty_object['broker'].get('email')[0])
            except User.DoesNotExist:
                try:
                    user = User.objects.create(
                        email=realty_object['broker'].get('email')[0],
                        first_name=str(realty_object['broker'].get('broker_name')).split(' ')[0],
                        last_name=str(realty_object['broker'].get('broker_name')).split(' ')[1],
                        username=realty_object['broker'].get('email')[0]
                    )
                except IntegrityError:
                    user = User.objects.create(
                        email=realty_object['broker'].get('email')[0],
                        first_name=str(realty_object['broker'].get('broker_name')).split(' ')[0],
                        last_name=str(realty_object['broker'].get('broker_name')).split(' ')[1],
                        username=str(realty_object['broker'].get('broker_name')).split(' ')[0]
                                 + realty_object['broker'].get('email')[0]
                    )
            profile = Profile.objects.get(user=user)
            profile.phone = realty_object['broker'].get('mobile')
            profile.access_level = 'AGENT'
            profile.save()
            agency.agents.add(profile)
            agency.save()
            realty_obj.agency = agency
            realty_obj.user = user
            realty_obj.save()
            iii+=1
