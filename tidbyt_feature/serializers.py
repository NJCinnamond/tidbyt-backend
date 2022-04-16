from rest_framework import serializers

from tidbyt_feature.models import TidbytFeature
from tidbyt_feature.services import FeatureService


class FeatureCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    text = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    feature_type = serializers.CharField(max_length=3)

    # Image and text are optional based on feature type so define a custom validator
    def validate(self, data):
        if not data.get('name', None):
            raise serializers.ValidationError('Name is required')

        if data.get('feature_type', None) == 'MM':
            if not data.get('text', None):
                raise serializers.ValidationError('Text is required for Morning Message')
        elif data.get('feature_type', None) == 'POD':
            if not data.get('image', None):
                raise serializers.ValidationError('Image is required for Picture of Day')
        else:
            raise serializers.ValidationError('Feature type is missing or invalid')

        return data


class FeatureUpdateSerializer(FeatureCreateSerializer, serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    feature_type = serializers.CharField(max_length=3, required=False)


class FeatureReadSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        feature_svc = FeatureService()
        image = feature_svc.generate_image_feature_string_from_obj(instance)

        return {
            'id': instance.id,
            'name': instance.name,
            "creator": instance.creator.id, #TODO: Replace this with UserSerializer
            'image': image,
            'feature_type': instance.feature_type, #TODO: Replace this with FeatureTypeSerializer
            "created_at": instance.created_at,
            "updated_at": instance.updated_at
        }