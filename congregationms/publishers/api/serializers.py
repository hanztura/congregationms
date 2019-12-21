from rest_framework import serializers

from publishers.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id', 'name', 'congregation', 'color']
