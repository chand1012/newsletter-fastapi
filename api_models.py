from pydantic import BaseModel

class MailSubscriber(BaseModel):
    email: str

class NewPost(BaseModel):
    title: str
    body: str
    