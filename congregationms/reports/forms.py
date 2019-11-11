from django.forms import ModelForm

from .models import MonthlyFieldService
from .utils import get_previous_month_end


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
        super().__init__(*args, **kwargs)
        self.fields['month_ending'].initial = get_previous_month_end()

    def save(self, commit=True):
        mfs = super().save(commit=False)

        group = mfs.publisher.group
        if mfs.group != group:
            mfs.group = group

        # check if publisher is RP
        is_rp = mfs.publisher.is_rp(mfs.month_ending)
        if is_rp:
            mfs.pioneering = mfs.publisher.pioneering.get_active_rp_detail(mfs.month_ending)

        mfs.save()

        return mfs
