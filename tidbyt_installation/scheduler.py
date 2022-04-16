from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import register_events, register_job

import logging

from .jobs.jobs import install_job, uninstall_job

# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


def start():
    if settings.DEBUG:
        # Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger("apscheduler").setLevel(logging.DEBUG)

    # TODO: Add cron job that ensures all TidbytInstallations have correctly scheduled jobs
    scheduler.add_job(
        func=install_job,
        trigger=IntervalTrigger(seconds=5),
        id="install_job",
        replace_existing=True,
    )

    scheduler.add_job(
        func=uninstall_job,
        trigger=IntervalTrigger(seconds=5),
        id="uninstall_job",
        replace_existing=True,
    )

    # Add the scheduled jobs to the Django admin interface
    register_events(scheduler)

    scheduler.start()
