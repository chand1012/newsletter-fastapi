import os
from typing import Optional
from secrets import token_urlsafe

from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.responses import Response

from database import Subscriber, Keys
from api_models import MailSubscriber

#Database Setup
db_url = os.environ.get("JAWSDB_URL")
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

# FastAPI Setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")

#endpoints
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    '''
    Index HTML Page
    '''
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/confirmation', response_class=HTMLResponse)
async def confirm_please(request: Request):
    '''
    Please confirm request.
    '''
    return templates.TemplateResponse("subscription.html", {"request": request})

@app.get("/ping")
async def ping():
    '''
    Test ping. Always returns "pong".
    '''
    return "pong"

@app.get('/already', response_class=HTMLResponse)
async def already(request: Request):
    '''
    Already subscribed.
    '''
    return templates.TemplateResponse("already.html", {"request": request})

@app.post("/subscribe")
async def subscribe(email: str = Form(...)):
    key = token_urlsafe(50)
    
    try:
        new_subscriber = Subscriber(email=email, key=key)
        session.add(new_subscriber)
        session.commit()
    except IntegrityError:
        return RedirectResponse('/already', 302)
        
    return RedirectResponse('/confirmation', 302)

@app.get("/confirm/{key}")
async def confirm(request: Request, key: str):
    sub = session.query(Subscriber).filter_by(key=key).first()
    if sub is None:
        return Response("404: User Not Found.", 404)
    sub.verified = 1
    session.commit()
    return templates.TemplateResponse("confirm.html", {"request": request, "email": sub.email})