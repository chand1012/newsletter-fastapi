import os
from secrets import token_urlsafe

from fastapi import Depends, FastAPI, Form, HTTPException, Request, Security
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.security.api_key import APIKey, APIKeyHeader
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_403_FORBIDDEN

from api_models import NewPost
from database import (get_subscriber, get_subscribers, query_subscriber, remove_all_unverified,
                      set_subscriber)
from mail import check, send_confirm_email, send_notification_email

API_KEY = os.environ.get('API_KEY')
API_KEY_NAME = "X-Api-Key"
COOKIE_DOMAIN = os.environ.get('COOKIE_DOMAIN')

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):

    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

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
    return templates.TemplateResponse("index.html", {"request": request, 'confirmation': True})

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
    return templates.TemplateResponse("index.html", {"request": request, 'already': True})

@app.get('/invalid', response_class=HTMLResponse)
async def invalid(request: Request):
    '''
    Invalid Email.
    '''
    return templates.TemplateResponse("index.html", {"request": request, "invalid": True})

@app.post("/subscribe")
async def subscribe(email: str = Form(...)):
    key = token_urlsafe(35)
    
    valid = check(email)

    if not valid:
        return RedirectResponse('/invalid', 302)

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
    return templates.TemplateResponse("index.html", {"request": request, "email": sub.get('key')})

@app.post("/new_post")
async def new_post(post: NewPost, api_key: APIKey = Depends(get_api_key)):
    emails = get_subscribers()
    send_notification_email(emails, post.title, post.body)
    return Response(content="{}", status_code=200)

@app.get("/clear_stale")
async def clear_stale(api_key: APIKey = Depends(get_api_key)):
    '''
    Clears all unverified emails from the database.
    '''
    remove_all_unverified()
    return Response(content="{}", status_code=200)