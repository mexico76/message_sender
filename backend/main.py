from typing import Optional
from fastapi import FastAPI, Response, Depends, status
from sqlalchemy.orm import Session
from schemas import ClientInfoIn, MailingInfoIn
from database import SessionLocal, engine
import models


from crud import (add_client, edit_client, remove_client, add_mailing,
                get_main_statistic, get_statistic_by_id,
                update_mailing_by_id, delete_mailing_by_id)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/client/",
          status_code=status.HTTP_201_CREATED,)
async def create_client(request: ClientInfoIn,
               db: Session = Depends(get_db)):
    add_client(request=request, db=db)
    return Response(status_code=status.HTTP_201_CREATED)


@app.put("/api/client/{client_id}",
         status_code=status.HTTP_204_NO_CONTENT,)
async def update_client(client_id: int, request: ClientInfoIn,
               db: Session = Depends(get_db)):
    edit_client(client_id=client_id, request=request, db=db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/api/client/{client_id}",
         status_code=status.HTTP_200_OK,)
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    remove_client(client_id=client_id, db=db)
    return Response(status_code=status.HTTP_200_OK)


@app.post("/api/mailing/",
          status_code=status.HTTP_200_OK,)
async def create_mailing(request: MailingInfoIn,
               db: Session = Depends(get_db)):
    return add_mailing(request=request, db=db)



@app.put("/api/mailing/{mailing_id}/",
          status_code=status.HTTP_204_NO_CONTENT,)
async def update_mailing(mailing_id:int, request: MailingInfoIn,
                        db: Session = Depends(get_db)):
    update_mailing_by_id(mailing_id=mailing_id, db=db,
                                request=request)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/api/mailing/{mailing_id}/",
          status_code=status.HTTP_200_OK,)
async def delete_mailing(mailing_id:int,  db: Session = Depends(get_db)):
    delete_mailing_by_id(mailing_id=mailing_id, db=db)


@app.get("/api/stat/main/",
          status_code=status.HTTP_200_OK,)
async def get_main_stat(db: Session = Depends(get_db)):
    return get_main_statistic( db=db)


@app.get("/api/stat/{mailing_id}/",
          status_code=status.HTTP_200_OK,)
async def get_stat_by_id(mailing_id:int, db: Session = Depends(get_db)):
    return get_statistic_by_id(mailing_id=mailing_id, db=db)

