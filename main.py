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
from database import get_subscribers, get_subscriber, query_subscriber, set_subscriber
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
    key = token_urlsafe(35)
    
    sub = get_subscriber(email)

    if not sub is None:
        return RedirectResponse('/already', 302)

    set_subscriber(email, key)
    send_confirm_email(email, key)
    return RedirectResponse('/confirmation', 302)

@app.get("/confirm/{key}")
async def confirm(request: Request, key: str):
    sub = query_subscriber(key)
    if sub is None:
        return Response('404: Error Not Found.', status_code=404)
    set_subscriber(sub.get('key'), sub.get('confirm_key'), verified=True)
    return templates.TemplateResponse("confirm.html", {"request": request, "email": sub.get('key')})

@app.post("/new_post")
async def new_post(post: NewPost):
    emails = get_subscribers()
    send_notification_email(emails, post.title, post.body)
    return Response(content="{}", status_code=200)
