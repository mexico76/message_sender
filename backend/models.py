
import datetime
import enum
from sqlalchemy import (Boolean, Column, Integer, String, Float, JSON, Numeric,
                        Date, Enum, ForeignKey, Time, DateTime, Table)
from sqlalchemy.orm import relationship

from database import Base



class Mailing(Base):
    """Модель рассылки"""
    __tablename__ = "mailings"

    id = Column(Integer, primary_key=True, index=True)
    date_time_start = Column(DateTime)
    message_text = Column(String, nullable=False)
    mob_code_filter = Column(String)
    tag_filter = Column(String)
    date_time_end = Column(DateTime)
    task_id = Column(String, nullable=True)
    messages = relationship("Message", back_populates="mailing")

    

class Client(Base):
    """Модель клиента"""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(Integer)
    phone_code = Column(String)
    tag = Column(String)
    time_zone = Column(String)
    message = relationship("Message", back_populates="client")

class Message(Base):
    """Модель сообщения"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    date_time_create = Column(DateTime)
    send_status = Column(Boolean, default=False)
    mailing_id = Column(Integer, ForeignKey("mailings.id"), )
    mailing = relationship("Mailing", back_populates="messages")
    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="message")
