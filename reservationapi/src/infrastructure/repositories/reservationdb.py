"""Module containing company reservation repository database implementation."""

from typing import Any, Iterable
from datetime import date

from asyncpg import Record  # type: ignore
from sqlalchemy import select, and_, func, case

from src.core.domain.reservation import ReservationStatusUpdateIn, ReservationStatus, ReservationBroker
from src.core.repositories.ireservation import IReservationRepository
from src.db import reservation_table, user_table, company_table, company_service_table, employee_table, database, \
    company_subcategory_table, category_table, account_table

RESERVATION_SORT_ORDER = case(
    (reservation_table.c.status == "Pending approval", "1"),
    (reservation_table.c.status == "Confirmed", "2"),
    (reservation_table.c.status == "Completed", "3"),
    (reservation_table.c.status == "Cancelled", "4"),
)

class ReservationRepository(IReservationRepository):
    """An implementation of repository class for reservation."""


    async def create_reservation(self, data: ReservationBroker) -> Any | None:
        """The method adding new reservation to the data.

        Args:
            data (ReservationBroker): The attributes of the reservation.

        Returns:
            Any | None: The newly created reservation.
        """

        insert_data = data.model_dump()
        insert_data["status"] = data.status.value

        query = reservation_table.insert().values(**insert_data)
        new_reservation = await database.execute(query)

        return await self.get_reservation_by_id(new_reservation)

    async def get_booked_slots_by_employee_and_date(self, employee_id: int, day: date) -> Iterable[Any]:
        """The abstract getting booked reservation for employee by day

        Args:
            employee_id (int): The id of the employee.
            day (date): TThe day to check

        Returns:
            Iterable[Any]: The collection of the all booked reservation for employee by day
        """

        query = (
            reservation_table.select()
            .where(
                and_(
                    reservation_table.c.employee_id == employee_id,
                    func.date(reservation_table.c.start_time) == day,
                    reservation_table.c.status != ReservationStatus.CANCELLED.value,
                    reservation_table.c.status != ReservationStatus.COMPLETED.value
                )
            )
            .order_by(reservation_table.c.start_time.asc())
        )
        return await database.fetch_all(query)

    async def get_reservation_by_id(self, reservation_id: int) -> Any | None:
        """The abstract getting a reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Any | None: The reservation data if exists.
        """

        client_account = account_table.alias("client_account")
        company_account = account_table.alias("company_account")

        query = (
            select(reservation_table, user_table, client_account, company_service_table,
                   company_subcategory_table,company_table, category_table,
                   company_account, employee_table
            )
            .select_from(
                reservation_table
                .outerjoin(user_table, reservation_table.c.client_id == user_table.c.id)
                .outerjoin(client_account, user_table.c.account_id == client_account.c.id)
                .join(company_service_table, reservation_table.c.service_id == company_service_table.c.id)
                .join(company_subcategory_table, company_service_table.c.subcategory_id == company_subcategory_table.c.id)
                .join(company_table, reservation_table.c.company_id == company_table.c.id)
                .join(category_table, company_table.c.category_id == category_table.c.id)
                .join(company_account, company_table.c.account_id == company_account.c.id)
                .join(employee_table, reservation_table.c.employee_id == employee_table.c.id)
            )
            .where(reservation_table.c.id == reservation_id) #type: ignore
            .order_by(reservation_table.c.id.asc())
        )

        reservation = await database.fetch_one(query)

        return reservation if reservation else None


    async def get_reservations_for_client(self, client_id: int) -> Iterable[Any]:
        """The abstract getting all reservations for client from the data storage.

        Args:
            client_id (int): The id of the client.

        Returns:
            Iterable[Any]: The collection of the all reservation by user id
        """

        query = (
            select(reservation_table, company_service_table)
            .select_from(
                reservation_table
                .join(company_service_table, reservation_table.c.service_id == company_service_table.c.id)
            )
        .where(reservation_table.c.client_id == client_id) #type: ignore
        .order_by(
                RESERVATION_SORT_ORDER.asc(),
                reservation_table.c.start_time.asc()
            )
        )

        return await database.fetch_all(query)

    async def get_reservations_for_company(self, company_id: int) -> Iterable[Any]:
        """The abstract getting all reservations for company from the data storage.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[Any]: The collection of the all reservation by company id
        """

        query = (
            select(reservation_table, company_service_table)
            .select_from(
                reservation_table
                .join(company_service_table, reservation_table.c.service_id == company_service_table.c.id)
            )
        .where(reservation_table.c.company_id == company_id) #type: ignore
        .order_by(
                RESERVATION_SORT_ORDER.asc(),
                reservation_table.c.start_time.asc()
            )
        )

        return await database.fetch_all(query)


    async def get_reservations_for_employee(self, employee_id) -> Iterable[Any]:
        """The abstract getting all reservations for employee from the data storage.

        Args:
            employee_id (int): The id of the employee.

        Returns:
            Iterable[Any]: The collection of the all reservation by employee id
        """

        query = (
            select(reservation_table, company_service_table)
            .select_from(
                reservation_table
                .join(company_service_table, reservation_table.c.service_id == company_service_table.c.id)
            )
        .where(reservation_table.c.employee_id == employee_id) #type: ignore
        .order_by(
                RESERVATION_SORT_ORDER.asc(),
                reservation_table.c.start_time.asc()
            )
        )

        return await database.fetch_all(query)

    async def update_status_reservation(self, reservation_id: int, data: ReservationStatusUpdateIn) -> Any | None:
        """The abstract updating reservation status in the reservation.

         Args:
             reservation_id (int): The id of the reservation.
             data (ReservationStatusUpdateIn): The details of the updated reservation status.

         Returns:
            Any | None: The updated reservation.
         """

        if await self.get_reservation_by_id(reservation_id=reservation_id):
            query = (
                reservation_table.update()
                .where(reservation_table.c.id == reservation_id)
                .values(status=data.status.value, updated_date=func.now())
            )
            await database.execute(query)

            reservation = await self.get_reservation_by_id(reservation_id=reservation_id)

            return reservation

        return None
