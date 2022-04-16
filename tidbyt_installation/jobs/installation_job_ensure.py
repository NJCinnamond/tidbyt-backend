from .installation_job_scheduler import InstallationJobScheduler

# TODO: Right now this schedules new jobs on every call.
# Make this smarter so it only schedules new jobs if there are no existing
# jobs for the installation at the correct time.
class InstallationJobEnsure(object):
    scheduler = InstallationJobScheduler()

    def ensure_pending_install_job(self, installation: object):
        print("IN INSTALLATION JOB ENSURE")
        if installation.install_time:
            self.scheduler.schedule_pending_install_job(
                installation, installation.install_time
            )

    def ensure_pending_uninstall_job(self, installation: object):
        if installation.uninstall_time:
            self.scheduler.schedule_pending_uninstall_job(
                installation, installation.uninstall_time
            )
