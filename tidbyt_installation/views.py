from django.http import Http404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from tidbyt_installation.serializers import (
    InstallationCreateSerializer,
    InstallationUpdateSerializer,
    InstallationReadSerializer,
)
from tidbyt_installation.services import InstallationService, InstallationCreateFailure
from tidbyt_installation.models import TidbytInstallation


class InstallationViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling Installation CRUD operations
    """

    read_serializer_class = InstallationReadSerializer
    create_serializer_class = InstallationCreateSerializer
    update_serializer_class = InstallationUpdateSerializer

    def list(self, request):
        queryset = TidbytInstallation.objects.all()
        serializer = self.read_serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            queryset = TidbytInstallation.objects.get(pk=pk)
        except TidbytInstallation.DoesNotExist as e:
            return Response(
                {"error": "Error reading installation: {}".format(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.read_serializer_class(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.create_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            installation_svc = InstallationService()
            installation_obj = installation_svc.create_installation(
                device_id=data.get("device_id", None),
                feature_id=data.get("feature_id", None),
                install_time=data.get("install_time", None),
                uninstall_time=data.get("uninstall_time", None),
                date=data.get("date", None),
            )
        except InstallationCreateFailure as e:
            return Response(
                {"error": "Error creating installation: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": "Unknown error: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        read_serializer = self.read_serializer_class(installation_obj)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            instance = TidbytInstallation.objects.get(pk=pk)
        except TidbytInstallation.DoesNotExist as e:
            return Response(
                {"error": "Error updating installation: {}".format(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.update_serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            installation_svc = InstallationService()
            installation_svc = installation_svc.update_installation(
                installation=instance,
                install_time=data.get("install_time", None),
                uninstall_time=data.get("uninstall_time", None),
                date=data.get("date", None),
            )
        except Exception as e:
            return Response(
                {"error": "Unknown error: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        read_serializer = self.read_serializer_class(instance)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            queryset = TidbytInstallation.objects.get(pk=pk)
        except TidbytInstallation.DoesNotExist as e:
            return Response(
                {"error": "Error deleting installation: {}".format(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            installation_svc = InstallationService()
            installation_svc = installation_svc.delete_installation(queryset)
        except Exception as e:
            return Response(
                {"error": "Unknown error: {}".format(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
