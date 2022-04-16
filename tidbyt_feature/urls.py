from rest_framework import routers

from tidbyt_feature.views import FeatureViewSet

FeatureRouter = routers.SimpleRouter()
FeatureRouter.register(r'features', FeatureViewSet, basename='feature')
 