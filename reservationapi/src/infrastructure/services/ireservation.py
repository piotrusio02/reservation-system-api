"""A module containing reservation service."""

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Iterable

from pydantic import UUID4

from src.core.domain.reservation import ReservationStatus, ReservationIn, ReservationBroker, Reservation, ReservationStatusUpdateIn
from src.infrastructure.dto.reservationdto import ReservationDTO
from src.infrastructure.dto.employeedto import EmployeeDTO, EmployeePublicDTO


class IReservationService(ABC):
    """An abstract class for reservation service."""

    @abstractmethod
    async def create_reservation(self, account_id: UUID4, role:str, data: ReservationIn) -> ReservationDTO | None:
        """The abstract creating new reservation.

        Args:
            account_id (UUID4): The account id of the user or company.
            role (str): The account role of the user or company.
            data (ReservationIn): The attributes of the reservation

        Returns:
            ReservationDTO | None: The reservation DTO model.
        """

    @abstractmethod
    async def get_reservation_by_id(self, account_id: UUID4, reservation_id: int) -> ReservationDTO | None:
        """The abstract getting a reservation from the data storage.

        Args:
            account_id (UUID4): The account id of the user or company.
            reservation_id (int): The id of the reservation.

        Returns:
            ReservationDTO | None: The reservation DTO model.
        """

    @abstractmethod
    async def get_client_reservations(self, account_id: UUID4) -> Iterable[ReservationDTO] | None:
        """The abstract getting all actual and history reservation by provided user.

        Args:
             account_id (UUID4): The account id of the user.

        Returns:
            Iterable[ReservationDTO]: The collection of the all user reservations.
        """

    @abstractmethod
    async def get_company_reservations(self, account_id: UUID4) -> Iterable[ReservationDTO] | None:
        """The abstract getting all actual and history reservation by provided company.

        Args:
             account_id (UUID4): The account id of the company.

        Returns:
            Iterable[ReservationDTO]: The collection of the all company reservations.
        """

    @abstractmethod
    async def get_employee_reservations(self, account_id: UUID4, employee_id: int) -> Iterable[ReservationDTO] | None:
        """The abstract getting all actual and history reservation by provided employee.

        Args:
             account_id (UUID4): The account id of the company.
             employee_id (int): The id of the employee.

        Returns:
            Iterable[ReservationDTO]: The collection of the all employee reservations.
        """

    @abstractmethod
    async def update_reservation_status(self, account_id: UUID4, reservation_id: int, data: ReservationStatusUpdateIn) -> ReservationDTO | None:
        """The abstract updating status reservation information.

        Args:
            account_id (UUID4): The account id of the company.
            reservation_id (int): The id of the reservation.
            data (ReservationStatusUpdateIn): The new reservation status information

        Returns:
            ReservationDTO | None: The updated reservation details.
        """

    @abstractmethod
    async def get_available_slots_service(self, employee_id: int, service_id: int, day: date) -> Iterable[datetime]:
        """The abstract getting all available date slots by employee, service and working day company.

        Args:
             employee_id (int): The id of the employee.
             service_id (int): The id of the service.
             day (date): Company opening day.

        Returns:
            Iterable[datetime]: The collection of the all available date slots.
        """