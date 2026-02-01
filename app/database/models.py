from sqlalchemy import Boolean, Column, DateTime, Integer
from app.database.database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    contact: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean)


class Texts(Base):
    __tablename__ = "users"
    name: Mapped[int] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
