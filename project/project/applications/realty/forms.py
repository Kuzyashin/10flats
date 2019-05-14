from django.forms import ModelForm
from dal import autocomplete
from .models import RealtyComplex


class RealtyComplexForm(ModelForm):
    class Meta:
        model = RealtyComplex
        fields = [
            'city',
            'area',
        ]
        widgets = {
            'city': autocomplete.ModelSelect2(url='city_name_lookup', forward=['region']),
            'area': autocomplete.ModelSelect2(url='area_name_lookup', forward=['city']),
        }

    def __init__(self, *args, **kwargs):
        super(RealtyComplexForm, self).__init__(*args, **kwargs)
        # self.fields['address'].widget.choices = [[self.instance.address, self.instance.address]]
