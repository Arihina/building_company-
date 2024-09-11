import datetime

from pydantic import BaseModel


class EmployeeDto(BaseModel):
    id: int
    post: str
    phone_number: str
    full_name: str
    email: str

    class Config:
        from_attributes = True


class ClientDto(BaseModel):
    id: int
    phone_number: str
    full_name: str
    organization_name: str | None

    class Config:
        from_attributes = True


class ProductDto(BaseModel):
    id: int
    type: str
    name: str
    price: float
    unit_type: str

    class Config:
        from_attributes = True


class DriverDto(BaseModel):
    id: int
    phone_number: str
    full_name: str
    car_type: str

    class Config:
        from_attributes = True


class WarehouseDto(BaseModel):
    id: int
    product_id: int
    quantity: int
    address: str

    class Config:
        from_attributes = True


class ConsistDto(BaseModel):
    id: int
    product_id: int
    data: datetime.datetime
    order_amount: float
    account_number: str

    class Config:
        from_attributes = True


class ContractDto(BaseModel):
    id: int
    contract_consist_id: int
    client_id: int
    employee_id: int

    class Config:
        from_attributes = True


class OrdersDto(BaseModel):
    id: int
    contract_id: int
    warehouse_id: int
    delivery_address: str
    driver_id: int
    prepayment: float
    product_volume: int
    status: bool

    class Config:
        from_attributes = True


class ManagerDto(BaseModel):
    phone_number: str
    full_name: str
    email: str

    class Config:
        from_attributes = True


class OrderDto(BaseModel):
    id: int
    client_name: str
    driver_name: str
    product_name: str
    product_volume: int
    data: datetime.datetime
    deliver_address: str
    warehouse_address: str
    order_amount: float


class ClientJoinDto(BaseModel):
    full_name: str
    phone_number: str
    organization_name: str | None


class NewOrderDto(BaseModel):
    client_name: str | None
    product_name: str | None
    driver_name: str | None
    client_id: int | None
    product_id: int | None
    driver_id: int | None
    warehouse_id: int
    delivery_address: str
    data: datetime.datetime
    order_amount: float
    prepayment: float
    account_number: str
    product_volume: int
