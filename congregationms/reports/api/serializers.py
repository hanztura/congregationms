from rest_framework import serializers

from reports.models import MonthlyFieldService


class MFSSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyFieldService
        fields = [
            'id',
            'publisher',
            'group',
            'pioneering',
            'month_ending',
            'placements',
            'video_showing',
            'hours',
            'return_visits',
            'bible_study',
            'comments',
        ]
