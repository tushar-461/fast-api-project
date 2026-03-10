from pydantic import BaseModel
from typing import List, Optional


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class CustomerBase(BaseModel):
    name: str
    age: int
    country: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    item: str
    amount: int
    shipping_status: str
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True


class OrderJoined(BaseModel):
    name: str
    age: int
    country: str
    item: str
    amount: int
    shipping_status: str

    class Config:
        orm_mode = True
