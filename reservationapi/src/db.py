"""A module providing database access"""

from enum import Enum

import asyncio

import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Enum as SQLEnum
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

from src.config import config
from src.core.domain.working_day import WeekDay
from src.core.domain.account import Role
from src.core.domain.reservation import ReservationStatus

metadata = sqlalchemy.MetaData()

account_table = sqlalchemy.Table(
    "accounts",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    ),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("phone_number", sqlalchemy.String, unique=False, nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("role", SQLEnum(Role, name="role_enum", values_callable=lambda obj: [e.value for e in obj]), nullable=False),
    sqlalchemy.Column("registration_date", sqlalchemy.DateTime, nullable=False)
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False),
    sqlalchemy.Column("account_id", UUID(as_uuid=True), sqlalchemy.ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("first_name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("last_name", sqlalchemy.String, nullable=False)
)

company_table = sqlalchemy.Table(
    "companies",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False),
    sqlalchemy.Column("account_id", UUID(as_uuid=True), sqlalchemy.ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("city", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("postal_code", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("street", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("category_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True)
)

category_table = sqlalchemy.Table(
    "categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
)

working_day_table = sqlalchemy.Table(
    "working_days",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("day", SQLEnum(WeekDay, name="day_enum", values_callable=lambda obj: [e.value for e in obj]), nullable=False),
    sqlalchemy.Column("opening_time", sqlalchemy.Time, nullable=True),
    sqlalchemy.Column("closing_time", sqlalchemy.Time, nullable=True),

    sqlalchemy.UniqueConstraint("company_id", "day", name="uix_1"),
)

employee_table = sqlalchemy.Table(
    "employees",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("first_name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("last_name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("phone_number", sqlalchemy.String, unique=False, nullable=False),
)

company_subcategory_table = sqlalchemy.Table(
    "company_subcategories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
)

company_service_table = sqlalchemy.Table(
    "company_services",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("subcategory_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("company_subcategories.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("duration_minutes", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("is_active", sqlalchemy.BOOLEAN, default=False)
)

service_employee_table = sqlalchemy.Table(
    "service_employee",
    metadata,
    sqlalchemy.Column("service_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("company_services.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("employee_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False),

    sqlalchemy.PrimaryKeyConstraint("service_id", "employee_id"),
)

reservation_table = sqlalchemy.Table(
    "reservations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("client_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),nullable=True),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("service_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("company_services.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("employee_id", sqlalchemy.Integer,sqlalchemy.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("start_time", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("end_time", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("status", SQLEnum(ReservationStatus, name="reservation_enum", values_callable=lambda obj: [e.value for e in obj]), nullable=False),
    sqlalchemy.Column("note", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("updated_date", sqlalchemy.DateTime, nullable=True)
)

db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    #force_rollback=True,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)

                await conn.execute(category_table.insert(),
                                   [{"name": "Fryzjer"},
                                    {"name": "Barber shop"},
                                    {"name": "Salon kosmetyczny"},
                                    {"name": "Paznokcie"},
                                    {"name": "Masaż"},
                                    {"name": "Zwierzaki"},
                                    {"name": "Tatuaż i Piercing"},
                                    {"name": "Motoryzacja"},
                                    ])
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
            OSError,
            ConnectionError
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")