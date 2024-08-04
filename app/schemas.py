from pydantic import BaseModel


class EmployeeSchema(BaseModel):
    id: int
    post: str
    phone_number: str
    full_name: str
    email: str

    class Config:
        from_attributes = True
