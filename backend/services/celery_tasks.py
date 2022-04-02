from fastapi import Depends
from datetime import datetime
import requests
from .celery import celeryapp
from models import Client, Message

from settings import token
from database import SessionLocal

# to start celery worker
# celery -A services worker -l INFO
# to start beat
# celery -A services beat -l INFO
# http://127.0.0.1:5555


@celeryapp.task
def shedule_sending(mailing:dict):
    db = SessionLocal()
    mailing_clients = db.query(Client).filter(
        Client.phone_code == mailing.get("mob_code_filter"),
        Client.tag == mailing.get("tag_filter")).all()

    date_time_end = datetime.strptime(mailing.get("date_time_end"), '%Y-%m-%dT%H:%M:%S.%f')
    sending_count = 0
    messages = []
    for client in mailing_clients:
        if datetime.now()< date_time_end:
            new_message = Message(
                date_time_create=datetime.now(),
                send_status=False,
                mailing_id=mailing.get("id"),
                client_id=client.id
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)
            messages.append(new_message.id)
            header = {"Authorization": "Bearer " + token}
            link = f"https://probe.fbrq.cloud/v1/send/{new_message.id}"
            response = requests.post(url=link, headers=header,
                    json={"id": new_message.id, "phone": client.phone,
                    "text": mailing.get("message_text")
                    })
            if response.status_code == 200:
                sending_count+=1
                new_message.send_status = True
                db.commit()
                db.refresh(new_message)
        else:
            break
    db.close()
    return f"finished! {sending_count} messages send. {messages}/ {mailing_clients}"