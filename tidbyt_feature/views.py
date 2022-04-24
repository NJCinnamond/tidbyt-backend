from django.http import Http404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from tidbyt_feature.serializers import (
    FeatureCreateSerializer,
    FeatureUpdateSerializer,
    FeatureReadSerializer,
)
from tidbyt_feature.services import (
    FeatureService,
    FeatureDeleteFailure,
    FeatureUpdateFailure,
    FeatureCreateFailure,
)
from tidbyt_feature.mixins import FeatureReadWriteSerializerMixin
from tidbyt_feature.models import TidbytFeature


class FeatureViewSet(FeatureReadWriteSerializerMixin, viewsets.ViewSet):
    """
    A ViewSet for handling Feature CRUD operations
    """

    read_serializer_class = FeatureReadSerializer
    create_serializer_class = FeatureCreateSerializer
    update_serializer_class = FeatureUpdateSerializer

    def list(self, request):  # GET to /features
        queryset = TidbytFeature.objects.all()
        serializer = self.read_serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):  # GET to /features/{pk}
        try:
            queryset = TidbytFeature.objects.get(pk=pk)
        except TidbytFeature.DoesNotExist as e:
            return Response(
                {"error": "Error reading feature: {}".format(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.read_serializer_class(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):  # POST to /features
        serializer = self.create_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            feature_svc = FeatureService()
            feature_obj = feature_svc.create_feature(
                name=data.get("name", None),
                creator_id=1,  # TODO: Change back to request.user.id
                image=data.get("image", None),
                text=data.get("text", None),
                feature_type=data.get("feature_type", None),
            )
        except FeatureCreateFailure as e:
            return Response(
                {"error": "Error creating feature: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": "Unknown error: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        read_serializer = self.read_serializer_class(feature_obj)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):  # PUT to /features/{pk}
        try:
            instance = TidbytFeature.objects.get(pk=pk)
        except TidbytFeature.DoesNotExist as e:
            return Response(
                {"error": "Error updating feature: {}".format(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.update_serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            feature_svc = FeatureService()
            feature_obj = feature_svc.update_feature(
                feature=instance,
                name=data.get("name", None),
                image=data.get("image", None),
                text=data.get("text", None),
            )
        except FeatureUpdateFailure as e:
            return Response(
                {"error": "Error updating feature: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": "Unknown error: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        read_serializer = self.read_serializer_class(feature_obj)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):  # Delete to /features/{pk}
        try:
            queryset = TidbytFeature.objects.get(pk=pk)
        except TidbytFeature.DoesNotExist as e:
            return Response(
                {"error": "Error deleting feature: {}".format(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            feature_svc = FeatureService()
            feature_svc.delete_feature(
                queryset, request.data.get("uninstall_from_all_devices")
            )
        except FeatureDeleteFailure as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": "Unknown error: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
