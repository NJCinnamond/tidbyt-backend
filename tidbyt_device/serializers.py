from rest_framework import serializers


class DeviceUpdateSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=100, required=False)
    device_name = serializers.CharField(max_length=100, required=False)
    auth_code = serializers.CharField(required=False)


class DeviceCreateSerializer(DeviceUpdateSerializer, serializers.Serializer):
    def validate(self, data):
        if not data.get("device_id", None):
            raise serializers.ValidationError("Device ID is required")

        if not data.get("device_name", None):
            raise serializers.ValidationError("Device name is required")

        if not data.get("auth_code", None):
            raise serializers.ValidationError("Auth code is required.")

        return data


class DeviceReadSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "tidbyt_id": instance.device_id,
            "name": instance.device_name,
            "owener": instance.owner.id,  # TODO: Replace this with UserSerializer
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }
