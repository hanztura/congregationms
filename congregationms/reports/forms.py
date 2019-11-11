from django.forms import ModelForm

from .models import MonthlyFieldService
from .utils import get_previous_month_end
from publishers.utils import get_publishers_as_choices


class MFSForm(ModelForm):

    class Meta:
        model = MonthlyFieldService
        fields = [
            'publisher',
            'month_ending',
            'placements',
            'video_showing',
            'hours',
            'return_visits',
            'bible_study',
            'comments'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['month_ending'].initial = get_previous_month_end()

        group = user.publisher.group
        publishers = []
        if group:
            # get publishers as choices
            publishers = get_publishers_as_choices(group=group)
        self.fields['publisher'].choices = publishers

    def save(self, commit=True):
        mfs = super().save(commit=False)

        group = mfs.publisher.group
        if mfs.group != group:
            mfs.group = group

        # check if publisher is pioneer
        is_pioneer = mfs.publisher.is_pioneer
        if is_pioneer:
            mfs.pioneering = mfs.publisher.pioneering.get_active_pioneer_detail(mfs.month_ending)

        mfs.save()

        return mfs
