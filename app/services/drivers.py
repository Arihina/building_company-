from sqlalchemy import select

from .. import db
from ..models import Driver
from ..schemas import DriverDto


class DriverService:
    @staticmethod
    def get_driver_by_name(name: str) -> Driver:
        return Driver.query().select().where(Driver.full_name == name)

    @staticmethod
    def get_drivers() -> list[dict]:
        query = (
            select(Driver)
        )
        drivers = db.session.execute(query).scalars().all()
        drivers_dto = [
            DriverDto.from_orm(driver).dict() for driver in drivers
        ]

        return drivers_dto
