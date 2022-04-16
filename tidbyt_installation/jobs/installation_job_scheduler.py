from django.conf import settings

from django_apscheduler.models import DjangoJob, DjangoJobExecution

from .jobs import pending_install_job, pending_uninstall_job
from tidbyt_installation.scheduler import scheduler

from datetime import datetime


class InstallationJobScheduler:
    scheduler = scheduler

    def schedule_pending_install_job(
        self, installation: object, install_time: datetime
    ):
        job_id = "pending_install_job_" + str(installation.id)

        # If the job is already scheduled, update the install time
        if DjangoJobExecution.objects.filter(job_id=job_id).exists():
            DjangoJobExecution.objects.get(job_id=job_id).run_time = install_time
            return

        # If the job is not scheduled, schedule it
        self.scheduler.add_job(
            pending_install_job,  # TODO: Add pending_install job
            "date",
            args=[installation],
            run_date=install_time,
            id=job_id,  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,  # TODO: Does this mean we can delete above?
        )

    def schedule_pending_uninstall_job(
        self, installation: object, uninstall_time: datetime
    ):
        job_id = "pending_uninstall_job_" + str(installation.id)

        # If the job is already scheduled, update the install time
        if DjangoJobExecution.objects.filter(job_id=job_id).exists():
            DjangoJobExecution.objects.get(job_id=job_id).run_time = uninstall_time
            return

        # If the job is not scheduled, schedule it
        self.scheduler.add_job(
            pending_uninstall_job,
            "date",
            args=[installation],
            run_date=uninstall_time,
            id=job_id,  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,  # TODO: Does this mean we can delete above?
        )
