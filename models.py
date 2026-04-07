from typing import Annotated

from sqlmodel import Field, Session, SQLModel, create_engine, select


class Track(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, )
    title: str = Field(..., max_length=100, min_length=1, title='Назва треку', index=True)
    artist: str = Field(..., max_length=100, min_length=2, index=True)
    album: str = Field(..., max_length=100, min_length=2, index=True)
    genre: str = Field(..., max_length=50, min_length=2, index=True)
    year: int = Field(..., ge=1900, le=2100)


class TrackUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=100, min_length=1, title='Назва треку')
    artist: str | None = Field(default=None, max_length=100, min_length=2)
    album: str | None = Field(default=None, max_length=100, min_length=2)
    genre: str | None = Field(default=None, max_length=50, min_length=2)
    year: int | None = Field(default=None, ge=1900, le=2100)

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, )
    login: str = Field(..., max_length=50, min_length=3, index=True, unique=True)
    password: str = Field(..., max_length=100, min_length=6)

