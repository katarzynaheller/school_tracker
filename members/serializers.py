from rest_framework import serializers

from .models import Child, Parent, Group


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "full_name",
            "age",
            "parent",
        )
        model = Child


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "user",
            "child",
        )
        model = Parent

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "members",
            "teacher",
            "group_name"
        )
        model = Group