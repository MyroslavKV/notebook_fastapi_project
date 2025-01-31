from datetime import datetime

from sqlalchemy import Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings import Base
from app.schemas import UserType


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserType] = mapped_column(default=UserType.USER)
    bio: Mapped[str] = mapped_column(nullable=True)

    create_date: Mapped[datetime] = mapped_column(server_default=func.now())

    notes = relationship("Note", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")

    def __str__(self):
        return f"User: {self.email}, {self.username}"


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="notes")

    comments = relationship("Comment", back_populates="note", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="comments")

    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"), nullable=False)
    note = relationship("Note", back_populates="comments")
