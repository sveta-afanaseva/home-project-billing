from sqlalchemy import Column, Integer

from app.sql_app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False, default=0, server_default="0")
