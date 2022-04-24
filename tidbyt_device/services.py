from django.core.files import File

from tidbyt_device.models import TidbytDevice

from user.models import User


class DeviceService(object):
    def create_device(
        self, device_name: str, device_id: str, owner_id: int, auth_code: str
    ) -> object:
        try:
            owner = User.objects.get(id=owner_id)
        except:
            raise DeviceCreateFailure("Creator does not exist")

        device_obj = TidbytDevice.objects.create(
            device_name=device_name,
            device_id=device_id,
            owner=owner,
            auth_code=auth_code,
        )
        device_obj.save()
        return device_obj

    def update_device(
        self,
        device: object,
        device_name: str,
        device_id: str,
        owner_id: int,
        auth_code: str,
    ) -> object:
        if device_name:
            device.device_name = device_name
        if device_id:
            device.device_id = device_id
        if owner_id:
            try:
                owner = User.objects.get(id=owner_id)
            except:
                raise DeviceUpdateFailure("Creator does not exist")
            device.owner = owner
        if auth_code:
            device.auth_code = auth_code

        try:
            device.save()
        except Exception as e:
            raise DeviceUpdateFailure(e)
        return device

    def delete_device(self, device: object):
        try:
            device.delete()
        except Exception as e:
            raise DeviceDeleteFailure(e)


class DeviceCreateFailure(BaseException):
    pass


class DeviceUpdateFailure(BaseException):
    pass


class DeviceDeleteFailure(BaseException):
    pass
