from rest_framework import routers

from tidbyt_installation.views import InstallationViewSet

InstallationRouter = routers.SimpleRouter()
InstallationRouter.register(r'installations', InstallationViewSet, basename='installation')