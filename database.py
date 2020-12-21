from sqlalchemy import String, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ORM Class for getting and setting subscribers
class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    verified = Column(Integer, default=0)
    key = Column(Integer)

    def __repr__(self) -> str:
        return f"<Subscriber({self.email})>"

# API Keys for sending out mass requests
class Keys(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    key = Column(String)

    def __repr__(self) -> str:
        return f"<Keys({self.id})>"