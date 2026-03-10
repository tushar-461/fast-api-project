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
    first_name: str
    last_name: str
    age: int
    country: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    customer_id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    item: str
    amount: int
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    order_id: int

    class Config:
        orm_mode = True


class ShippingBase(BaseModel):
    status: str
    customer_id: Optional[int] = None


class ShippingCreate(ShippingBase):
    pass


class Shipping(ShippingBase):
    shipping_id: int

    class Config:
        orm_mode = True


class OrderJoined(BaseModel):
    first_name: str
    last_name: str
    age: int
    country: str
    item: str
    amount: int
    shipping_status: Optional[str] = None

    class Config:
        orm_mode = True
