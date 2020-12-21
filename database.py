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


# class Keys(Base):
#     __tablename__ = "api_keys"

#     id = Column(Integer, primary_key=True)
#     client_key = Column(String)
#     email = Column(String)