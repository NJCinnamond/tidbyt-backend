from django.urls import path
from rest_framework import routers

from tidbyt_device.views import DeviceViewSet

DeviceRouter = routers.SimpleRouter()
DeviceRouter.register(r"devices", DeviceViewSet, basename="device")
