from django.http import Http404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response

from tidbyt_device.serializers import (
    DeviceCreateSerializer,
    DeviceUpdateSerializer,
    DeviceReadSerializer,
)
from tidbyt_device.services import (
    DeviceService,
    DeviceCreateFailure,
    DeviceUpdateFailure,
    DeviceDeleteFailure,
)
from tidbyt_device.mixins import DeviceReadWriteSerializerMixin
from tidbyt_device.models import TidbytDevice
from tidbyt_installation.models import TidbytInstallation
from tidbyt_installation.serializers import InstallationReadSerializer


class DeviceViewSet(DeviceReadWriteSerializerMixin, viewsets.ViewSet):
    """
    A ViewSet for handling device CRUD operations
    """

    read_serializer_class = DeviceReadSerializer
    create_serializer_class = DeviceCreateSerializer
    update_serializer_class = DeviceUpdateSerializer

    def list(self, request):  # GET to /devices
        queryset = TidbytDevice.objects.all()
        serializer = self.read_serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):  # GET to /devices/{pk}
        try:
            queryset = TidbytDevice.objects.get(pk=pk)
        except TidbytDevice.DoesNotExist as e:
            return Response(
                {"error": "Error reading device: {}".format(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.read_serializer_class(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):  # POST to /devices
        serializer = self.create_serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            device_svc = DeviceService()
            device_obj = device_svc.create_device(
                device_name=data.get("device_name", None),
                device_id=data.get("device_id", None),
                owner_id=1,  # TODO: Change back to request.user.id
                auth_code=data.get("auth_code", None),
            )
        except DeviceCreateFailure as e:
            return Response(
                {"error": "Error creating device: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": "Unknown error: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        read_serializer = self.read_serializer_class(device_obj)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):  # PUT to /devices/{pk}
        try:
            instance = TidbytDevice.objects.get(pk=pk)
        except TidbytDevice.DoesNotExist as e:
            return Response(
                {"error": "Error updating device: {}".format(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.update_serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            device_svc = DeviceService()
            device_obj = device_svc.update_device(
                instance,
                device_name=data.get("device_name", None),
                device_id=data.get("device_id", None),
                owner_id=1,  # TODO: Change back to request.user.id
                auth_code=data.get("auth_code", None),
            )
        except DeviceUpdateFailure as e:
            return Response(
                {"error": "Error updating device: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": "Unknown error: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        read_serializer = self.read_serializer_class(device_obj)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):  # Delete to /devices/{pk}
        try:
            queryset = TidbytDevice.objects.get(pk=pk)
        except TidbytDevice.DoesNotExist as e:
            return Response(
                {"error": "Error deleting device: {}".format(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            device_svc = DeviceService()
            device_svc.delete_device(queryset)
        except DeviceDeleteFailure as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": "Unknown error: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=True, url_path="installations")
    def get_installations(self, request, pk=None):  # GET to /devices/{pk}/installations
        try:
            device_obj = TidbytDevice.objects.get(pk=pk)
        except TidbytDevice.DoesNotExist as e:
            return Response(
                {"error": "Error getting device: {}".format(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            queryset = TidbytInstallation.objects.filter(device=device_obj)
            serializer = InstallationReadSerializer(queryset)
        except Exception as e:
            return Response(
                {"error": "Unknown error: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
