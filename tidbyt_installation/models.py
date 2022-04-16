from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class InstallationStatus(models.TextChoices):
    INSTALLED = "IN", ("Installed")
    UNINSTALLED = "UN", ("Uninstalled")
    PENDING_INSTALL = "PI", ("Pending Install")
    PENDING_UNINSTALL = "PU", ("Pending Uninstall")


class TidbytInstallation(models.Model):
    installation_id = models.CharField(max_length=100)
    device = models.ForeignKey("tidbyt_device.TidbytDevice", on_delete=models.CASCADE)
    feature = models.OneToOneField(
        "tidbyt_feature.TidbytFeature", on_delete=models.CASCADE
    )
    install_time = models.DateTimeField(blank=True, null=True)
    uninstall_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    installation_status = models.CharField(
        max_length=2,
        choices=InstallationStatus.choices,
        default=InstallationStatus.UNINSTALLED,
    )
