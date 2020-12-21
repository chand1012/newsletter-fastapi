from pydantic import BaseModel

class MailSubscriber(BaseModel):
    email: str
