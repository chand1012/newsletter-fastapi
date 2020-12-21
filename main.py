import os
from typing import Optional

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

engine = os.environ.get("JAWSDB_MARIA_URL")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index():
    return templates.TemplateResponse("index.html")
