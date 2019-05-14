from celery import Celery
from celery.schedules import crontab


def init_celery(app, celery_app):
    """ Used to instantiate celery in the main application."""

    celery_app.__init__(
        main=app.import_name,
        backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery_app.conf.update(app.config)

    celery_app.conf.task_routes = {
        'approve-user': {'queue': 'altmetrics.approve-user'},
        'send-approval-request': {'queue': 'altmetrics.send-approval-request'},
        'pull-metrics': {'queue': 'altmetrics.pull-metrics'},
        'process-plugin': {'queue': 'altmetrics.process-plugin'},
        'send-metrics': {'queue': 'altmetrics.send-metrics'},
    }


def make_celery(app):
    """Used to instantiate celery in the workers."""

    celery_app = Celery(
        app.import_name,
        backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery_app.conf.update(app.config)

    TaskBase = celery_app.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask

    return celery_app


def configure_celery(celery_app):
    """Add configuration for celery tasks."""

    celery_app.conf.beat_schedule = {
        'pull-metrics-every-day': {
            'task': 'pull-metrics',
            'schedule': crontab(minute=0, hour=12, day_of_week='*')
        },
        'send-metrics-every-day': {
            'task': 'send-metrics',
            'schedule': crontab(minute=0, hour=18, day_of_week='*')
        },
        'check-wikipedia-references-every-day': {
            'task': 'check-wikipedia-references',
            'schedule': crontab(minute=0, hour=10, day_of_week='*')
        },
        'check-deleted-wikipedia-references-every-day': {
            'task': 'check-deleted-wikipedia-references',
            'schedule': crontab(minute=0, hour=11, day_of_week='*')
        },
    }

    celery_app.conf.task_routes = {
        'approve-user': {'queue': 'altmetrics.approve-user'},
        'send-approval-request': {'queue': 'altmetrics.send-approval-request'},
        'pull-metrics': {'queue': 'altmetrics.pull-metrics'},
        'process-plugin': {'queue': 'altmetrics.process-plugin'},
        'check-wikipedia-references': {'queue': 'altmetrics.plugin-admin'},
        'check-deleted-wikipedia-references': {
            'queue': 'altmetrics.plugin-admin'
        },
        'send-metrics': {'queue': 'altmetrics.send-metrics'},
    }
