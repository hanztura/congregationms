from django.forms import ModelForm, ValidationError
from django.forms.models import inlineformset_factory

from .models import Group, Member, Publisher


class PublisherModelForm(ModelForm):

    class Meta:
        model = Publisher
        fields = ['last_name', 'first_name', 'middle_name',
                  'date_of_birth', 'date_of_baptism', 'contact_numbers',
                  'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = True

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Publisher.objects.filter(slug=slug):
            message = 'Sorry this slug already exists, please use another.'
            raise ValidationError(message)
        return slug


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
    extra=3, can_delete=True
)
