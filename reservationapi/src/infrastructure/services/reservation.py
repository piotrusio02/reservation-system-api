"""A module containing reservation service."""

from typing import Iterable
from datetime import date, datetime, timedelta

from pydantic import UUID4

from src.core.domain.reservation import ReservationIn, ReservationStatusUpdateIn, ReservationStatus, ReservationBroker
from src.core.domain.account import Role
from src.core.repositories.ireservation import IReservationRepository
from src.core.repositories.icompany import ICompanyRepository
from src.core.repositories.iuser import IUserRepository
from src.core.repositories.icompany_service import ICompanyServiceRepository
from src.core.repositories.iworking_day import IWorkingDayRepository
from src.core.repositories.iemployee import IEmployeeRepository
from src.infrastructure.dto.reservationdto import ReservationDTO, ReservationListDTO
from src.infrastructure.services.ireservation import IReservationService

class ReservationService(IReservationService):
    """A class implementing the reservation service."""

    _s_repository: ICompanyServiceRepository
    _c_repository: ICompanyRepository
    _u_repository: IUserRepository
    _r_repository: IReservationRepository
    _w_repository: IWorkingDayRepository
    _e_repository: IEmployeeRepository


    def __init__(self, s_repository: ICompanyServiceRepository, c_repository: ICompanyRepository,
                 u_repository: IUserRepository, r_repository: IReservationRepository,
                 w_repository: IWorkingDayRepository, e_repository: IEmployeeRepository) -> None:
        """The initializer of the employee service.

        Args:
            s_repository (ICompanyServiceRepository): The reference to the company service repository.
            c_repository (ICompanyRepository): The reference to the company repository.
            u_repository (IUserRepository): The reference to the user repository.
            r_repository (IReservationRepository): The reference to the reservation repository.
            w_repository (IWorkingDayRepository): The reference to the working day repository.
            e_repository (IEmployeeRepository): The reference to the employee repository.
        """

        self._s_repository = s_repository
        self._c_repository = c_repository
        self._u_repository = u_repository
        self._r_repository = r_repository
        self._w_repository = w_repository
        self._e_repository = e_repository

    async def create_reservation(self, account_id: UUID4, role: str, data: ReservationIn) -> ReservationDTO | None:
        """The method creating new reservation.

        Args:
            account_id (UUID4): The account id of the user.
            role (str): The account role of the user or company.
            data (ReservationIn): The attributes of the reservation

        Returns:
            ReservationDTO | None: The reservation DTO model.
        """

        if role == Role.USER.value:
            client_id = await self._get_user_id(account_id=account_id)
            if not client_id:
                return None
            status = ReservationStatus.PENDING
        else:
            client_id = None
            status = ReservationStatus.CONFIRMED

        service = await self._s_repository.get_service_by_id(service_id=data.service_id)
        if not service:
            return None

        available_slots = await self.get_available_slots_service(employee_id=data.employee_id, service_id=data.service_id,
                                                                 day=data.start_time.date())
        if not available_slots:
            return None


        if data.start_time not in available_slots:
            return None

        end_time = data.start_time + timedelta(minutes=service["duration_minutes"])

        reservation = ReservationBroker(
            client_id=client_id,
            company_id=service["company_id"],
            service_id=data.service_id,
            employee_id=data.employee_id,
            start_time=data.start_time,
            end_time=end_time,
            status=status,
            note=data.note,
            created_date=datetime.now()
        )

        new_reservation = await self._r_repository.create_reservation(data=reservation)

        if not new_reservation:
            return None

        return ReservationDTO.from_record(new_reservation)


    async def get_reservation_by_id(self, account_id: UUID4, reservation_id: int) -> ReservationDTO | None:
        """The method getting a reservation from the data storage.

        Args:
            account_id (UUID4): The account id of the user or company.
            reservation_id (int): The id of the reservation.

        Returns:
            ReservationDTO | None: The reservation DTO model.
        """

        reservation = await self._r_repository.get_reservation_by_id(reservation_id=reservation_id)
        if not reservation:
            return None

        client_id = await self._get_user_id(account_id=account_id)
        company_id = await self._get_company_id(account_id=account_id)

        if company_id is not None and reservation["company_id"] == company_id:
            return ReservationDTO.from_record(reservation)

        if client_id is not None and reservation["client_id"] == client_id:
            return ReservationDTO.from_record(reservation)

        return None

    async def get_client_reservations(self, account_id: UUID4) -> Iterable[ReservationListDTO] | None:
        """The method getting all actual and history reservation by provided user.

        Args:
             account_id (UUID4): The account id of the user.

        Returns:
            Iterable[ReservationListDTO]: The collection of the all user reservations.
        """

        client_id = await self._get_user_id(account_id=account_id)
        if not client_id:
            return None

        reservations = await self._r_repository.get_reservations_for_client(client_id=client_id)

        return [ReservationListDTO.from_record(reservation) for reservation in reservations]

    async def get_company_reservations(self, account_id: UUID4) -> Iterable[ReservationListDTO] | None:
        """The method getting all actual and history reservation by provided company.

        Args:
             account_id (UUID4): The account id of the company.

        Returns:
            Iterable[ReservationListDTO]: The collection of the all company reservations.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        reservations = await self._r_repository.get_reservations_for_company(company_id=company_id)

        return [ReservationListDTO.from_record(reservation) for reservation in reservations]

    async def get_employee_reservations(self, account_id: UUID4, employee_id: int) -> Iterable[ReservationListDTO] | None:
        """The method getting all actual and history reservation by provided employee.

        Args:
             account_id (UUID4): The account id of the company.
             employee_id (int): The id of the employee.

        Returns:
            Iterable[ReservationListDTO]: The collection of the all employee reservations.
        """

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id:
            return None

        employee = await self._e_repository.get_employee_by_id(company_id=company_id,employee_id=employee_id)
        if not employee:
            return None

        reservations = await self._r_repository.get_reservations_for_employee(employee_id=employee_id)

        return [ReservationListDTO.from_record(reservation) for reservation in reservations]


    async def update_reservation_status(self, account_id: UUID4, reservation_id: int, data: ReservationStatusUpdateIn) -> ReservationDTO | None:
        """The method updating status reservation information.

        Args:
            account_id (UUID4): The account id of the company.
            reservation_id (int): The id of the reservation.
            data (ReservationStatusUpdateIn): The new reservation status information

        Returns:
            ReservationDTO | None: The updated reservation details.
        """

        reservation = await self._r_repository.get_reservation_by_id(reservation_id=reservation_id)
        if not reservation:
            return None

        if reservation["status"] == ReservationStatus.COMPLETED.value or reservation["status"] == ReservationStatus.CANCELLED.value:
            return None

        company_id = await self._get_company_id(account_id=account_id)
        if not company_id or reservation["company_id"] != company_id:
            return None

        updated_reservation = await self._r_repository.update_status_reservation(
            reservation_id=reservation_id,
            data=data
        )

        if not updated_reservation:
            return None

        return ReservationDTO.from_record(updated_reservation)

    async def get_available_slots_service(self, employee_id: int, service_id: int, day: date) -> Iterable[datetime] | None:
        """The method getting all available date slots by employee, service and working day company.

        Args:
             employee_id (int): The id of the employee.
             service_id (int): The id of the service.
             day (date): Company opening day.

        Returns:
            Iterable[datetime]: The collection of the all available date slots.
        """

        service = await self._s_repository.get_service_by_id(service_id=service_id)
        if not service:
            return None

        if not await self._is_employee_assigned(service_id=service_id, employee_id=employee_id):
            return None

        if day < date.today():
            return []

        duration = timedelta(minutes=service["duration_minutes"])
        company_id = service["company_id"]

        current_day = day.strftime("%A")

        working_days = await self._w_repository.get_by_company_id(company_id=company_id)

        current_working_day = None
        for working_day in working_days:
            if working_day["day"].value == current_day:
                current_working_day = working_day
                break

        if not current_working_day or current_working_day["opening_time"] is None or current_working_day["closing_time"] is None:
            return []

        start = datetime.combine(day, current_working_day["opening_time"])
        end = datetime.combine(day, current_working_day["closing_time"])

        booked_reservations = await self._r_repository.get_booked_slots_by_employee_and_date(employee_id=employee_id, day=day)

        available_slots = []
        current_time = start
        now = datetime.now()

        while current_time + duration <= end:
            if day == now.date() and current_time < now:
                current_time += timedelta(minutes=15)
                continue
            potential_end = current_time + duration

            is_unavailable = False
            for reservation in booked_reservations:
                if current_time < reservation["end_time"] and potential_end > reservation["start_time"]:
                    is_unavailable = True
                    break

            if not is_unavailable:
                available_slots.append(current_time)
            current_time += timedelta(minutes=15)

        return available_slots

    async def _get_company_id(self, account_id: UUID4) -> int | None:
        """A private method translating account ID to company ID.

        Args:
            account_id (UUID4): The account id of the company.

        Returns:
            int | None: The company ID
        """

        company = await self._c_repository.get_by_account_id(account_id)

        if not company:
            return None

        return company["id"]

    async def _get_user_id(self, account_id: UUID4) -> int | None:
        """A private method translating account ID to user ID.

        Args:
            account_id (UUID4): The account id of the user.

        Returns:
            int | None: The user ID
        """

        user = await self._u_repository.get_by_account_id(account_id)

        if not user:
            return None

        return user["id"]

    async def _is_employee_assigned(self, service_id: int, employee_id: int) -> bool:
        """A private method to check employee for specific service.

        Args:
            service_id (int): The id of the service.
            employee_id (int): The id of the employee.

        Returns:
            bool: True if the employee is assigned to the service
        """

        assigned_employees = await self._s_repository.get_employees_by_service_id_public(service_id=service_id)

        if not assigned_employees:
            return False

        for employee in assigned_employees:
            if employee["id"] == employee_id:
                return True

        return False