from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)
from sqlalchemy.sql.schema import MetaData


class Base(MappedAsDataclass, DeclarativeBase):
    # This map details the specific transformation of types between Python and
    # PostgreSQL. This is only needed for the case where a specific PostgreSQL
    # type has to be used or when we want to ensure a specific setting (like the
    # timezone below)
    type_annotation_map = {
        Dict[str, Any]: MutableDict.as_mutable(
            JSONB
        ),  # transform Python Dict[str, Any] into PostgreSQL JSONB
        List[Dict[str, Any]]: MutableList.as_mutable(JSONB),
        datetime: DateTime(
            timezone=False
        ),  # transform Python datetime into PostgreSQL Datetime without timezone
        List[str]: ARRAY(
            item_type=String
        ),  # transform Python List[str] into PostgreSQL Array of strings
    }

    # This metadata specifies some naming conventions that will be used by
    # alembic to generate constraints names (indexes, unique constraints, ...)
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
    pass


class User(Base):
    """
    User model, used for managing users.
    """

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    created_on: Mapped[datetime]

    projects: Mapped[List["Project"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", init=False
    )


class Project(Base):
    """
    Project model, used for managing projects.
    A Project is a group of files and archives.
    Project will be deleted after certain time.
    """

    __tablename__ = "projects"

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), init=False)
    name: Mapped[str]
    created_on: Mapped[datetime]
    expire_on: Mapped[Optional[datetime]]

    user: Mapped[User] = relationship(back_populates="projects", init=False)

    files: Mapped[List["File"]] = relationship()
    archives: Mapped[List["Archive"]] = relationship()


class File(Base):
    """
    File model, used for managing uploaded files.
    All binary files will not be stored in the database, but in the file system.
    The files will be saved as hash values to save space.
    """

    __tablename__ = "files"

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id"), init=False)

    filename: Mapped[str]
    filesize: Mapped[int]
    title: Mapped[str]
    authors: Mapped[Optional[List[str]]]
    description: Mapped[Optional[str]]
    uploaded_on: Mapped[datetime]
    hash: Mapped[str]
    path: Mapped[str]
    type: Mapped[str]
    status: Mapped[str]


class Archive(Base):
    """
    Archive model, used for managing archives.
    Arhcives are zim files and will be generated by zimfarm.
    All of the archives will be deleted after certain time.
    """

    __tablename__ = "archives"

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id"), init=False)

    filename: Mapped[str]
    filesize: Mapped[int]
    created_on: Mapped[datetime]
    requested_on: Mapped[datetime]
    download_url: Mapped[str]
    collection_json_path: Mapped[str]
    status: Mapped[str]
    zimfarm_task_id: Mapped[UUID]
    email: Mapped[Optional[str]]
    config: Mapped[Dict[str, Any]]
