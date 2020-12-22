import os
from secrets import token_urlsafe

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import session, sessionmaker
from starlette.responses import Response

from api_models import NewPost
from database import Subscriber
from mail import send_confirm_email, send_notification_email

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
    except IntegrityError as e:
        print(e)
        session.rollback()
        return RedirectResponse('/already', 302)
    
    send_confirm_email(email, key)
    return RedirectResponse('/confirmation', 302)

@app.get("/confirm/{key}")
async def confirm(request: Request, key: str):
    sub = session.query(Subscriber).filter_by(key=key).first()
    if sub is None:
        return Response("404: User Not Found.", 404)
    sub.verified = 1
    session.commit()
    return templates.TemplateResponse("confirm.html", {"request": request, "email": sub.email})

@app.post("/new_post")
async def new_post(post: NewPost):
    subs = session.query(Subscriber).all()
    emails = []
    for sub in subs:
        emails += [sub.email]
    
    send_notification_email(emails, post.title, post.body)
    return Response(content="{}", status_code=200)
