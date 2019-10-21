from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Pioneer, PioneerDetail

class PioneerDetailModelForm(ModelForm):


    class Meta:
        model = PioneerDetail
        fields = [
            'pioneer',
            'pioneer_type',
            'date_start',
            'date_end',
        ]


PioneerDetailFormSet = inlineformset_factory(
    Pioneer,
    PioneerDetail,
    form=PioneerDetailModelForm,
    fields=[
        'pioneer',
        'pioneer_type',
        'date_start',
        'date_end'],
    extra=1,
    can_delete=True
)
