from django.core.files import File

from tidbyt_feature.models import TidbytFeature

from tidbyt_installation.services import InstallationService
from images.services import ImageService

from user.models import User


class FeatureService(object):

    installation_svc = InstallationService()
    image_svc = ImageService()

    def create_feature(
        self, name: str, creator_id: int, image: str, text: str, feature_type: str
    ) -> object:
        try:
            creator = User.objects.get(id=creator_id)
        except:
            raise FeatureCreateFailure("Creator does not exist")

        image_obj = self.create_image_field(image, text)

        feature_obj = TidbytFeature.objects.create(
            name=name, creator=creator, feature_type=feature_type, text=text
        )
        feature_obj.image.save(
            "feature-img-{}.png".format(feature_obj.id), File(image_obj), save=False
        )
        feature_obj.save()
        return feature_obj

    def update_feature(
        self, feature: object, name: str, image: str, text: str
    ) -> object:
        if name:
            feature.name = name
        if image or text:
            image_obj = self.create_image_field(image, text)
            feature.text = text
            feature.image.save(
                "feature-img-{}.png".format(feature.id), File(image_obj), save=False
            )

        try:
            feature.save()
        except Exception as e:
            raise FeatureUpdateFailure(e)
        return feature

    def delete_feature(self, feature: object, uninstall_from_all_devices: bool):
        if uninstall_from_all_devices:
            # TODO: call installation service to uninstall from all devices
            pass

        try:
            feature.delete()
        except Exception as e:
            raise FeatureDeleteFailure(e)

    def create_image_field(self, image: str, text: str) -> object:
        if not image:
            if not text:
                return False
            return self.image_svc.generate_pil_from_text(text)

        return self.image_svc.generate_pil_from_base_64(image)

    def generate_image_feature_string_from_obj(self, feature_obj: object) -> str:
        return self.image_svc.generate_base_64_from_pil(feature_obj.image)


class FeatureCreateFailure(BaseException):
    pass


class FeatureUpdateFailure(BaseException):
    pass


class FeatureDeleteFailure(BaseException):
    pass
