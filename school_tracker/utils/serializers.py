from rest_framework import serializers


class ReadOnlyModelSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError("")

    def update(self, instance, validated_data):
        raise NotImplementedError("")