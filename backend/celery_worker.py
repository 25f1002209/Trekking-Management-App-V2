from celery import Celery
celery = Celery("treknologia")
celery.config_from_object("celery_config")
celery.conf.imports = ("tasks",)