from django.forms import ModelForm
from dal import autocomplete
from .models import RealtyComplex


class RealtyComplexForm(ModelForm):
    class Meta:
        model = RealtyComplex
        fields = [
            'name',
            'city',
            'area',
        ]
        widgets = {
            'name': autocomplete.ListSelect2(url='complex_name_lookup'),
            'city': autocomplete.ModelSelect2(url='city_name_lookup', forward=['region']),
            'area': autocomplete.ModelSelect2(url='area_name_lookup', forward=['city']),
        }

    def __init__(self, *args, **kwargs):
        super(RealtyComplexForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.choices = [[self.instance.name, self.instance.name]]
