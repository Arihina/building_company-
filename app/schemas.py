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
    organization_name: str

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
    product_name: str
    quantity: int
    address: str

    class Config:
        from_attributes = True
