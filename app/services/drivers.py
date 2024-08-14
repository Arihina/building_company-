from ..models import Driver


class DriverService:
    @staticmethod
    def get_driver_by_name(name: str) -> Driver:
        return Driver.query().select().where(Driver.full_name == name)
