"""Module containing reservation repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable
from datetime import date

from src.core.domain.reservation import ReservationIn, ReservationStatusUpdateIn

class IReservationRepository(ABC):
    """An abstract class representing protocol of reservation repository."""

    @abstractmethod
    async def create_reservation(self, data: ReservationIn) -> Any | None:
        """The abstract adding new reservation to the data.

        Args:
            data (ReservationIn): The attributes of the reservation.

        Returns:
            Any | None: The newly created reservation.
        """

    @abstractmethod
    async def get_booked_slots_by_employee_and_date(self, employee_id: int, day: date) -> Iterable[Any]:
        """The abstract getting booked reservation for employee by day

        Args:
            employee_id (int): The id of the employee.
            day (date): TThe day to check

        Returns:
            Iterable[Any]: The collection of the all booked reservation for employee by day
        """

    @abstractmethod
    async def get_reservation_by_id(self, reservation_id: int) -> Any | None:
        """The abstract getting a reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Any | None: The reservation data if exists.
        """
    @abstractmethod
    async def get_reservations_for_client(self, client_id: int) -> Iterable[Any]:
        """The abstract getting all reservations for client from the data storage.

        Args:
            client_id (int): The id of the client.

        Returns:
            Iterable[Any]: The collection of the all reservation by user id
        """
    @abstractmethod
    async def get_reservations_for_company(self, company_id: int) -> Iterable[Any]:
        """The abstract getting all reservations for company from the data storage.

        Args:
            company_id (int): The id of the company.

        Returns:
            Iterable[Any]: The collection of the all reservation by company id
        """
    @abstractmethod
    async def get_reservations_for_employee(self, employee_id) -> Iterable[Any]:
        """The abstract getting all reservations for employee from the data storage.

        Args:
            employee_id (int): The id of the employee.

        Returns:
            Iterable[Any]: The collection of the all reservation by employee id
        """
    @abstractmethod
    async def update_status_reservation(self, reservation_id: int, data: ReservationStatusUpdateIn) -> Any | None:
        """The abstract updating reservation status in the reservation.

         Args:
             reservation_id (int): The id of the reservation.
             data (ReservationStatusUpdateIn): The details of the updated reservation status.

         Returns:
            Any | None: The updated reservation.
         """