from celery import Celery
import settings


celeryapp = Celery("services", include=["services.celery_tasks"])
celeryapp.conf.broker_url = settings.CELERY_BROKER_URL
celeryapp.conf.result_backend = settings.CELERY_RESULT_BACKEND
celeryapp.conf.timezone = 'Europe/Moscow'
celeryapp.conf.enable_utc = True


if __name__ == '__main__':
    celeryapp.start()