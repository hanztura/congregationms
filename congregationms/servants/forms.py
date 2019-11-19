from django.forms import ModelForm, ChoiceField

from .models import Servant
from publishers.utils import get_publishers_as_choices


class ServantModelForm(ModelForm):
    servant_type = ChoiceField()

    class Meta:
        model = Servant
        fields = ['publisher', 'elder', 'ms']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servant_type'].required = True
        self.fields['servant_type'].choices = (
            ('elder', 'Elder'),
            ('ms', 'Ministerial Servant')
        )

        self.fields['publisher'].choices = get_publishers_as_choices()

    def clean(self):
        cleaned_data = super().clean()
        elder = cleaned_data['elder']
        ms = cleaned_data['ms']

        if elder:
            ms = not elder
        else:
            if ms:
                elder = not ms

        cleaned_data['elder'] = elder
        cleaned_data['ms'] = ms
        return cleaned_data
