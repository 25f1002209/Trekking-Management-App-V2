broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"

timezone = "Asia/Kolkata"

enable_utc = False

from celery.schedules import crontab

broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"

timezone = "Asia/Kolkata"
enable_utc = False

beat_schedule = {
    "daily-reminder": {
        "task": "tasks.daily_reminder_email",
        "schedule": crontab(hour=9, minute=0),
    },

    "monthly-report": {
        "task": "tasks.monthly_report",
        "schedule": crontab(hour=9, minute=0, day_of_month=1),
    },
}