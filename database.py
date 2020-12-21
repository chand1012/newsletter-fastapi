from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ORM Class for getting and setting subscribers
class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    verified = Column(Integer)
    key = Column(Integer)

# API Keys for sending out mass requests
class Keys(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    key = Column(String)
