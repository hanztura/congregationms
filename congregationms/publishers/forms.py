from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Group, Member


class GroupMemberForm(ModelForm):


    class Meta:
        model = Member
        fields = [
            'group',
            'publisher',
            'is_active',
            'date_from',
            'date_to'
        ]


GroupMemberFormSet = inlineformset_factory(
    Group, Member, form=GroupMemberForm,
    fields=['publisher', 'is_active', 'date_from', 'date_to'],
    extra=1, can_delete=True
)
