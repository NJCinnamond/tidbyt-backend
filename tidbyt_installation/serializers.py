from rest_framework import serializers

from tidbyt_installation.models import TidbytInstallation

from tidbyt_feature.serializers import FeatureReadSerializer


class InstallationUpdateSerializer(serializers.Serializer):
    install_time = serializers.DateTimeField(required=False)
    uninstall_time = serializers.DateTimeField(required=False)
    date = serializers.DateTimeField(required=False)

    def validate(self, data):
        if (data.get('install_time', None) and data.get('uninstall_time', None)):
            if data.get('install_time', None) > data.get('uninstall_time', None):
                raise serializers.ValidationError('Install time cannot be greater than uninstall time')
        #TODO: Date cannot be in past?
        #TODO: Object cannot be updated in PendingInstall or PendindUninstall status
        #TODO: Object's install time cannot be updated in Installed status
        return data


class InstallationCreateSerializer(InstallationUpdateSerializer, serializers.Serializer):
    device_id = serializers.IntegerField()
    feature_id = serializers.IntegerField()


class InstallationReadSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'installation_id': instance.installation_id,
            'install_time': instance.install_time,
            'uninstall_time': instance.uninstall_time,
            'installation_status': instance.installation_status,
            'feature': FeatureReadSerializer(instance.feature).data,
            'device_id': instance.device_id, #TODO: Create TidbytDeviceReadSerializer?
            "created_at": instance.created_at,
            "updated_at": instance.updated_at
        }