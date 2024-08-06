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
