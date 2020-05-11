from django.forms import ModelForm, ValidationError, BaseInlineFormSet
from django.forms.models import inlineformset_factory

from .models import Group, Member, Publisher
from .utils import get_groups_as_choices
from system.utils import compute_age, get_congregation_as_choices
from publishers.utils import get_publishers_as_choices


class PublisherModelForm(ModelForm):

    class Meta:
        model = Publisher
        fields = ['last_name', 'first_name', 'middle_name',
                  'date_of_birth', 'date_of_baptism', 'contact_numbers',
                  'slug', 'infirmed', 'elderly', 'male',
                  'assets', 'city', 'address_line_1', 'email_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = True
        self._low_case_fields = [
            'last_name', 'first_name', 'middle_name'
        ]

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        publisher = Publisher.objects.filter(slug=slug).first()
        if publisher:
            if publisher.pk != self.instance.pk:
                message = 'Sorry this slug already exists, please use another.'
                raise ValidationError(message)
        return slug

    def process_low_case_fields(self, data):
        fields = self._low_case_fields
        for field in fields:
            data[field] = data[field].lower()

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth', None)
        elderly = cleaned_data.get('elderly', False)

        if dob:
            age = compute_age(dob)
            elderly = age >= 60
            cleaned_data['elderly'] = elderly

        # low case necessary fields
        self.process_low_case_fields(cleaned_data)

        city = self.cleaned_data.get('city', None)
        address_line_1 = self.cleaned_data.get('address_line_1', None)
        if city and (not address_line_1):
            self.add_error('address_line_1', 'Please put address line.')

        return cleaned_data


class GroupModelForm(ModelForm):

    class Meta:
        model = Group
        fields = ['name', 'congregation', 'color']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['congregation'].choices = get_congregation_as_choices()
        self.fields['color'].required = True


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'].choices = get_publishers_as_choices()
        self.fields['is_active'].initial = True


GroupMemberFormSet = inlineformset_factory(
    Group, Member, form=GroupMemberForm,
    fields=['publisher', 'is_active', 'date_from', 'date_to'],
    extra=3, can_delete=True
)
