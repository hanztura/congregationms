from django.forms import ModelForm

from .models import MonthlyFieldService


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

    def save(self, commit=True):
        mfs = super().save(commit=False)

        group = mfs.publisher.group
        if mfs.group != group:
            mfs.group = group
        mfs.save()

        return mfs