from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Pioneer, PioneerDetail
from publishers.utils import get_publishers_as_choices


class PioneerModelForm(ModelForm):
    class Meta:
        model = Pioneer
        fields = [
            'publisher', 'code'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        group = user.publisher.group
        publishers = []
        if group:
            # get publishers as choices
            publishers = get_publishers_as_choices(group=group)
        self.fields['publisher'].choices = publishers


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
