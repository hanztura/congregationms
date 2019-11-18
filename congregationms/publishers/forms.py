from django.forms import ModelForm, ValidationError
from django.forms.models import inlineformset_factory

from .models import Group, Member, Publisher
from system.utils import compute_age


class PublisherModelForm(ModelForm):

    class Meta:
        model = Publisher
        fields = ['last_name', 'first_name', 'middle_name',
                  'date_of_birth', 'date_of_baptism', 'contact_numbers',
                  'slug', 'infirmed', 'elderly']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = True

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        publisher = Publisher.objects.filter(slug=slug).first()
        if publisher:
            if publisher.pk != self.instance.pk:
                message = 'Sorry this slug already exists, please use another.'
                raise ValidationError(message)
        return slug

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth', None)
        elderly = cleaned_data.get('elderly', False)

        if dob:
            age = compute_age(dob)
            elderly = age >= 60
            cleaned_data['elderly'] = elderly

        return cleaned_data


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
