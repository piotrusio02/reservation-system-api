"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from src.api.routers.account import router as account_router
from src.api.routers.user import router as user_router
from src.api.routers.company import router as company_router
from src.api.routers.category import router as category_router
from src.api.routers.working_day import router as working_day_router
from src.api.routers.employee import router as employee_router
from src.api.routers.company_subcategory import router as subcategory_router
from src.api.routers.company_service import router as service_router
from src.api.routers.reservation import router as reservation_router
from src.container import Container
from src.db import database, init_db

container = Container()
container.wire(modules=[
    "src.api.routers.account",
    "src.api.routers.user",
    "src.api.routers.company",
    "src.api.routers.category",
    "src.api.routers.working_day",
    "src.api.routers.employee",
    "src.api.routers.company_subcategory",
    "src.api.routers.company_service",
    "src.api.routers.reservation"
])

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(account_router, prefix="/accounts")
app.include_router(user_router, prefix="/users")
app.include_router(company_router, prefix="/companies")
app.include_router(category_router, prefix="/categories")
app.include_router(working_day_router, prefix="/working-days")
app.include_router(employee_router, prefix="/employees")
app.include_router(subcategory_router, prefix="/subcategories")
app.include_router(service_router, prefix="/services")
app.include_router(reservation_router, prefix="/reservations")

@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)