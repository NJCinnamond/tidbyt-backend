from django.conf import settings

from tidbyt_api.client import TidbytAPIClient
from tidbyt_installation.models import InstallationStatus, TidbytInstallation
from tidbyt_device.models import TidbytDevice

from images.services import ImageService

import hashlib
import datetime


def pending_install_job(installation: object):
    if installation.installation_status == InstallationStatus.PENDING_INSTALL:
        print(
            "Warning: Installation {} is already pending install".format(
                installation.id
            )
        )
        return

    installation.installation_status = InstallationStatus.PENDING_INSTALL
    installation.save()


def pending_uninstall_job(installation: object):
    if installation.installation_status == InstallationStatus.PENDING_INSTALL:
        print(
            "Warning: Installation {} is already pending uninstall".format(
                installation.id
            )
        )
        return

    installation.installation_status = InstallationStatus.PENDING_UNINSTALL
    installation.save()


# TODO: For below jobs, handle retries, create fn to deduce device installation id if not present


def install_job():
    """z
    The Install job runs continuously every x seconds and collects all TidbytInstallation objects
    in PENDING_INSTALL state and installs them to their device. This job defines the state
    transition from PENDING_INSTALL -> INSTALLED.
    """
    client = TidbytAPIClient(settings.TIDBYT_API_URL)
    objects_needing_install = TidbytInstallation.objects.filter(
        installation_status=InstallationStatus.PENDING_INSTALL
    )
    print("Objects needing install: ", objects_needing_install)
    for installation in objects_needing_install:
        # If an Installation ID is not present (i.e. if this installation hasn't been installed before)
        # we generate a new one using a hash fn
        if not installation.installation_id:
            installation.installation_id = generate_installation_id(installation)
            installation.save()

        device_obj = TidbytDevice.objects.get(id=installation.device_id)

        # Get Base64 string for feature image
        image = ImageService().generate_base_64_from_pil(installation.feature.image)

        resp = client.install_to_device(
            device_obj.device_id,
            device_obj.auth_code,
            installation.installation_id,
            image,
        )

        if int(resp.status) == 200:
            installation.installation_status = InstallationStatus.INSTALLED
            installation.save()
        else:
            installation.installation_status = InstallationStatus.UNINSTALLED
            installation.save()
            print(
                "Error: Installation {} failed to install to device {}".format(
                    installation.id, device_obj.id
                )
            )
            print("HTTP Error Code {}: {}".format(resp.status, resp.reason))


def uninstall_job():
    """
    The Uninstall job runs continuously every x seconds and collects all TidbytInstallation objects
    in PENDING_UNINSTALL state and installs them to their device. This job defines the state
    transition from PENDING_UNINSTALL -> UNINSTALLED.
    """
    client = TidbytAPIClient(settings.TIDBYT_API_URL)
    objects_needing_uninstall = TidbytInstallation.objects.filter(
        installation_status=InstallationStatus.PENDING_UNINSTALL
    )

    print("UNINSTALLING OBJECTS: ", objects_needing_uninstall)

    for installation in objects_needing_uninstall:
        device_obj = TidbytDevice.objects.get(id=installation.device_id)

        resp = client.uninstall_from_device(
            device_obj.device_id,
            device_obj.auth_code,
            installation.installation_id,
        )

        if int(resp.status) == 200:
            print("UNINSTALLATION SUCCESSFUL")
            installation.installation_status = InstallationStatus.UNINSTALLED
            installation.save()
        else:
            installation.installation_status = InstallationStatus.UNINSTALLED
            installation.save()
            print(
                "Error: Installation {} failed to uninstall from device {}.".format(
                    installation.id, device_obj.id
                )
            )
            print("HTTP Error Code {}: {}".format(resp.status, resp.reason))


def installation_consistency_job():
    """
    The Installation Consistency job is a periodic job that runs continuously every x seconds.
    It collects all TidbytDevice objects and queries the Tidbyt API for their installation IDs.

    The job compares the TidbytInstallation object's installation_id with the installation_id
    retrieved from the API. If they do not match, the job updates the TidbytInstallation object
    with the installation_id retrieved from the API.
    """
    client = TidbytAPIClient(settings.TIDBYT_API_URL)
    devices = TidbytDevice.objects.all()

    for device in devices:
        resp = client.get_installation_for_device(device.id, device.auth_code)

        if resp.status_code == 200:
            resp_json = resp.json()

            installation_ids_on_device = [
                installation["id"] for installation in resp_json
            ]

            # Iterate over all installations we believe are on the device
            # If an installation is not on the device, mark it as UNINSTALLED
            # and set deleteTime to null
            for installation in TidbytInstallation.objects.filter(device_id=device.id):
                if installation.installation_id not in installation_ids_on_device:
                    installation.installation_status = InstallationStatus.UNINSTALLED
                    installation.delete_time = None
                    installation.save()
                    print(
                        "Warning: Installation {} is not on device {}".format(
                            installation.id, device.id
                        )
                    )
        else:
            print(
                "Error: Failed to retrieve installation_id for device {}".format(
                    device.id
                )
            )
