from rest_framework import serializers

class UUIDField(serializers.UUIDField):
    def to_representation(self, value):
        return str(value.uuid)
