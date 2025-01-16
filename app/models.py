from datetime import datetime

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings import Base
from app.schemas import UserType

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[UserType] = mapped_column(default=UserType.USER)
    bio: Mapped[str] = mapped_column(nullable=True)
        
    notes = relationship("Notes", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comments", back_populates="author", cascade="all, delete-orphan")

class Notes():
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int]= mapped_column(ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="notes")
    comments = relationship("Comments", back_populates="note", cascade="all, delete-orphan")

class Comments():
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int]= mapped_column(ForeignKey("users.id"), nullable=False)
    note_id: Mapped[int]= mapped_column(ForeignKey("notes.id"), nullable=False)

    author = relationship("User", back_populates="comments")
    note = relationship("Notes", back_populates="comments")

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[int] = mapped_column(unique=True, nullable=False)
    note_id: Mapped[int]= mapped_column(ForeignKey("notes.id"), nullable=False)

    note = relationship("Notes", back_populates="tags")