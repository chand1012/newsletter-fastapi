import os
from typing import Optional
from secrets import token_urlsafe

from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

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

@app.post("/subscribe")
async def subscribe(email: str = Form(...)):
    key = token_urlsafe(50)
    new_subscriber = Subscriber(email=email, key=key)
    session.add(new_subscriber)
    session.commit()
    return RedirectResponse('/confirmation', 302)