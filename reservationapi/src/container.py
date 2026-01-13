"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.repositories.userdb import UserRepository
from src.infrastructure.repositories.categorydb import CategoryRepository
from src.infrastructure.repositories.accountdb import AccountRepository
from src.infrastructure.repositories.companydb import CompanyRepository
from src.infrastructure.repositories.working_daydb import WorkingDayRepository
from src.infrastructure.repositories.employeedb import EmployeeRepository
from src.infrastructure.repositories.company_subcategorydb import CompanySubcategoryRepository
from src.infrastructure.repositories.company_servicedb import CompanyServiceRepository
from src.infrastructure.repositories.reservationdb import ReservationRepository

from src.infrastructure.services.user import UserService
from src.infrastructure.services.category import CategoryService
from src.infrastructure.services.account import AccountService
from src.infrastructure.services.company import CompanyService
from src.infrastructure.services.working_day import WorkingDayService
from src.infrastructure.services.employee import EmployeeService
from src.infrastructure.services.company_subcategory import CompanySubcategoryService
from src.infrastructure.services.company_service import CompanyServiceService
from src.infrastructure.services.reservation import ReservationService

class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    user_repository = Singleton(UserRepository)
    category_repository = Singleton(CategoryRepository)
    account_repository = Singleton(AccountRepository)
    company_repository = Singleton(CompanyRepository)
    working_day_repository = Singleton(WorkingDayRepository)
    employee_repository = Singleton(EmployeeRepository)
    subcategory_repository = Singleton(CompanySubcategoryRepository)
    service_repository = Singleton(CompanyServiceRepository)
    reservation_repository = Singleton(ReservationRepository)


    user_service = Factory(
        UserService,
        repository=user_repository
    )
    category_service = Factory(
        CategoryService,
        repository=category_repository
    )
    account_service = Factory(
        AccountService,
        repository=account_repository
    )
    company_service = Factory(
        CompanyService,
        repository=company_repository,
        c_repository=category_repository
    )
    working_day_service = Factory(
        WorkingDayService,
        wd_repository=working_day_repository,
        c_repository=company_repository
    )
    employee_service = Factory(
        EmployeeService,
        e_repository=employee_repository,
        c_repository=company_repository
    )
    subcategory_service = Factory(
        CompanySubcategoryService,
        s_repository=subcategory_repository,
        c_repository=company_repository
    )
    service_service = Factory(
        CompanyServiceService,
        s_repository=service_repository,
        c_repository=company_repository,
        sc_repository=subcategory_repository,
        e_repository=employee_repository
    )
    reservation_service = Factory(
        ReservationService,
        s_repository=service_repository,
        c_repository=company_repository,
        u_repository=user_repository,
        r_repository=reservation_repository,
        w_repository=working_day_repository,
        e_repository=employee_repository
    )