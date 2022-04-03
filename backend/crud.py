from datetime import datetime
from pytz import timezone
from sqlalchemy.orm import Session, contains_eager, joinedload
from sqlalchemy import func, case
from  fastapi import HTTPException, status
from services.celery_tasks import shedule_sending
from services.celery import celeryapp

from models import Client, Mailing, Message
from schemas import ClientInfoIn, MailingInfoIn



def get_client(db:Session, client_id:int) -> Client:
    client_db = db.query(Client).filter(Client.id == client_id).first()
    if client_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Client was not found")
    return client_db


def get_mailing_by_id(db:Session, mailing_id:int) -> Mailing:
    mailing_db = db.query(Mailing).filter(Mailing.id == mailing_id).first()
    if mailing_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Mailing was not found")
    return mailing_db


def add_client(request:ClientInfoIn, db:Session):
    client = Client(
        phone=request.phone,
        phone_code=request.phone_code,
        tag=request.tag,
        time_zone=request.time_zone
    )
    db.add(client)
    db.commit()


def edit_client(client_id:int, request:ClientInfoIn, db:Session):
    client_db = get_client(db=db, client_id=client_id)
    client_db.phone = request.phone
    client_db.phone_code = request.phone_code
    client_db.tag = request.tag
    client_db.time_zone = request.time_zone
    db.commit()
    db.refresh(client_db)


def remove_client(client_id:int, db:Session):
    client_db = get_client(db=db, client_id=client_id)
    db.delete(client_db)
    db.commit()


def add_mailing(request:MailingInfoIn, db:Session):
    mailing = Mailing(
        date_time_start=request.date_time_start,
        message_text=request.message_text,
        mob_code_filter=request.mob_code_filter,
        tag_filter=request.tag_filter,
        date_time_end=request.date_time_end
    )
    db.add(mailing)
    db.commit()
    mailing_dict = {
        "id": mailing.id,
        "date_time_start": mailing.date_time_start,
        "message_text": mailing.message_text,
        "mob_code_filter": mailing.mob_code_filter,
        "tag_filter": mailing.tag_filter,
        "date_time_end": mailing.date_time_end
    }
    if datetime.now() >= mailing.date_time_start and\
        datetime.now() < mailing.date_time_end:
        task = shedule_sending.delay(mailing_dict)
        mailing.task_id = task.id
        db.commit()
        return {"info": f"Задача запущена на немедленное выполнение",
                "task_id": f"{task.id}"}
    elif datetime.now() < mailing.date_time_start:
        '''Выполнять отложенную задачу'''
        locale_to_use = timezone('Europe/Moscow')
        current_time = locale_to_use.localize(mailing.date_time_start)
        task = shedule_sending.apply_async((mailing_dict,), eta=current_time)
        mailing.task_id = task.id
        db.commit()
        db.refresh(mailing)
        return {"info": f"Задача будет выполнена {mailing.date_time_start}",
                "task_id": f"{task.id}"}
def update_mailing_by_id(mailing_id:int, db:Session, request:MailingInfoIn):
    mailing_db = get_mailing_by_id(db=db, mailing_id=mailing_id)
    if datetime.now() < request.date_time_start:
        """Изменить время старта рассылки в schedules"""
        celeryapp.control.revoke(mailing_db.task_id)
    mailing_db.date_time_start = request.date_time_start
    mailing_db.message_text = request.message_text
    mailing_db.mob_code_filter = request.mob_code_filter
    mailing_db.tag_filter = request.tag_filter
    mailing_db.date_time_end = request.date_time_end
    mailing_dict = {
        "id": mailing_db.id,
        "date_time_start": mailing_db.date_time_start,
        "message_text": mailing_db.message_text,
        "mob_code_filter": mailing_db.mob_code_filter,
        "tag_filter": mailing_db.tag_filter,
        "date_time_end": mailing_db.date_time_end
    }
    locale_to_use = timezone('Europe/Moscow')
    current_time = locale_to_use.localize(mailing.date_time_start)
    task = shedule_sending.apply_async((mailing_dict,), eta=current_time)
    mailing_db.task_id = task.id
    db.commit()
    db.refresh(mailing_db)
    return {"info": f"Задача будет выполнена {mailing_db.date_time_start}",
            "task_id": f"{task.id}"}


def delete_mailing_by_id(mailing_id:int, db:Session):
    mailing_db = get_mailing_by_id(db=db, mailing_id=mailing_id)
    """Удалить запланированное задание, привязанное к рассылке"""
    celeryapp.control.revoke(mailing_db.task_id)
    db.delete(mailing_db)
    db.commit()


def get_main_statistic(db:Session):
    mailing_db = db.query(Mailing, 
        func.coalesce((func.sum(case([(Message.send_status == True, 1)]))
            ), 0).label("count_true"),
        func.coalesce((func.sum(case([(Message.send_status == False, 1)]))
            ), 0).label("count_false"),
        ).outerjoin(Message
        ).group_by(Mailing.id
        ).all()
    return mailing_db


def get_statistic_by_id(db:Session, mailing_id:int):
    get_mailing_by_id(db=db, mailing_id=mailing_id)
    mailing = db.query(Mailing).options(joinedload(Mailing.messages)
        ).join(Message
        ).filter(Mailing.id == mailing_id).all()
    return mailing