from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Shipping(Base):
    __tablename__ = "shippings"

    shipping_id = Column(Integer, primary_key=True, index=True)
    status = Column(String(100))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))

    customer = relationship("Customer", back_populates="shipping")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), index=True)
    last_name = Column(String(100), index=True)
    age = Column(Integer)
    country = Column(String(100))

    orders = relationship("Order", back_populates="customer")
    shipping = relationship("Shipping", back_populates="customer", uselist=False)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    item = Column(String(100))
    amount = Column(Integer)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))

    customer = relationship("Customer", back_populates="orders")
