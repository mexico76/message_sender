DB_HOST = "fs_db"
DB_USER = "postgres" 
DB_PASS = "password"
DB_NAME = "sender_db"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODAxNzYyNDIsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Ik1pa2hhaWwifQ.imk76XDQq7vyomWF5hYVYjgbu7mUjOlJekfmmsPZO58"

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"