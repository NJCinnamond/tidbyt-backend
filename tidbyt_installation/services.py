from django.utils import timezone

from tidbyt_installation.models import InstallationStatus, TidbytInstallation
from tidbyt_installation.jobs.installation_job_ensure import InstallationJobEnsure

import datetime
import pytz
import hashlib


class InstallationService(object):
    job_ensurer = InstallationJobEnsure()
    utc = pytz.UTC

    def create_installation(
        self,
        device_id: int,
        feature_id: int,
        install_time: int,
        uninstall_time: int,
        date: str,
    ) -> object:
        # If a date is provided, override install and uninstall time
        if date:
            (
                install_time,
                uninstall_time,
            ) = self.create_install_and_uninstall_time_from_date(date)

        if not install_time and not date:
            raise InstallationCreateFailure("Install time or Date is required")

        # Ensure we have valid install and uninstall time
        install_time, uninstall_time = self.get_valid_install_and_uninstall_time(
            install_time, uninstall_time
        )

        installation_obj = TidbytInstallation.objects.create(
            device_id=device_id,
            feature_id=feature_id,
            install_time=install_time,
            uninstall_time=uninstall_time,
            installation_status=InstallationStatus.UNINSTALLED,
        )

        # Generate unique installation id
        installation_id = self.generate_installation_id(installation_obj)
        installation_obj.installation_id = installation_id

        self.job_ensurer.ensure_pending_install_job(installation_obj)
        self.job_ensurer.ensure_pending_uninstall_job(installation_obj)
        return installation_obj

    def update_installation(
        self, installation: object, install_time: int, uninstall_time: int, date: str
    ) -> object:
        # If a date is provided, override install and uninstall time
        if date:
            (
                install_time,
                uninstall_time,
            ) = self.create_install_and_uninstall_time_from_date(date)

        # Ensure we have valid install and uninstall time
        install_time, uninstall_time = self.get_valid_install_and_uninstall_time(
            install_time, uninstall_time
        )

        if install_time:
            installation.install_time = install_time
        if uninstall_time:
            installation.uninstall_time = uninstall_time

        installation.save()

        self.job_ensurer.ensure_pending_install_job(installation)
        self.job_ensurer.ensure_pending_uninstall_job(installation)
        return installation

    def delete_installation(self, installation: object):
        # TODO: Function to uninstall from all devices
        installation.delete()

    def get_valid_install_and_uninstall_time(
        self, install_time: int, uninstall_time: int
    ):
        if uninstall_time and install_time > uninstall_time:
            raise Exception("Install time cannot be after uninstall time")

        if install_time and install_time < timezone.now():
            install_time = datetime.datetime.now()
            # todo: run pending install job here
            # todo: OR schedule it for 30 secs in future?

        if uninstall_time and uninstall_time < timezone.now():
            uninstall_time = datetime.datetime.now()
            # todo: run pending uninstall job here
            # todo: OR schedule it for 30 secs in future?

        return install_time, uninstall_time

    def get_installations_for_device(self, device_id: int):
        return TidbytInstallation.objects.filter(device_id=device_id)

    def create_install_and_uninstall_time_from_date(self, date: datetime.datetime):
        # install_time = self.convert_datetime_to_utc(date)
        # uninstall_time = self.convert_datetime_to_utc(date.replace(hour=23, minute=59, second=59))
        # return install_time, uninstall_time
        return date, date.replace(hour=23, minute=59, second=59)

    def convert_datetime_to_utc(self, date: datetime.datetime) -> int:
        return (date - datetime(1970, 1, 1)).total_seconds()

    # TODO: Move this elsewhere
    def generate_installation_id(self, installation: object):
        feature_id = str(installation.feature.id).encode("utf-8")
        user_id = str(installation.device.owner.id).encode("utf-8")
        device_id = str(installation.device.device_id).encode("utf-8")
        date_str = str(datetime.datetime.now()).encode("utf-8")
        installation_id = hashlib.sha256(
            feature_id + user_id + device_id + date_str
        ).hexdigest()
        return installation_id[
            :10
        ]  # todo: make str more readable, maybe prepend with feature type?


class InstallationCreateFailure(BaseException):
    pass
