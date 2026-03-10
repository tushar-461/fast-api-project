from sqlalchemy.orm import Session
from . import models, schemas


def create_shipping(shipping: dict):
    db = SessionLocal()
    s = models.Shipping(**shipping)
    db.add(s)
    db.commit()
    db.refresh(s)
    db.close()
    return s
from .database import SessionLocal
import logging

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
log = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, username: str, password: str):
    hashed = pwd_context.hash(password)
    user = models.User(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    log.info("user_created username=%s", username)
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_customers(db: Session):
    return db.query(models.Customer).all()


def get_customer_by_fullname(db: Session, first: str, last: str):
    return db.query(models.Customer).filter(models.Customer.first_name == first, models.Customer.last_name == last).first()


def create_customer(customer: dict):
    db = SessionLocal()
    # expect keys first_name, last_name, age, country
    c = models.Customer(**customer)
    db.add(c)
    db.commit()
    db.refresh(c)
    db.close()
    return c


def get_orders_count():
    db = SessionLocal()
    count = db.query(models.Order).count()
    db.close()
    return count


def create_order(order: dict):
    db = SessionLocal()
    # allow either customer_id or first+last name lookup
    cust = None
    if order.get("customer_id"):
        cust = db.query(models.Customer).filter(models.Customer.customer_id == order["customer_id"]).first()
    elif order.get("customer_name"):
        # split by space
        parts = order["customer_name"].split()
        if len(parts) >= 2:
            cust = get_customer_by_fullname(db, parts[0], parts[1])
    if cust:
        o = models.Order(item=order["item"], amount=order["amount"], customer_id=cust.customer_id)
        db.add(o)
        db.commit()
        db.refresh(o)
        db.close()
        return o
    db.close()
    return None


def get_joined_orders(db: Session):
    # return list of orders with customer info and shipping status if available
    results = (
        db.query(
            models.Customer.first_name,
            models.Customer.last_name,
            models.Customer.age,
            models.Customer.country,
            models.Order.item,
            models.Order.amount,
            models.Shipping.status.label("shipping_status")
        )
        .join(models.Order, models.Customer.customer_id == models.Order.customer_id)
        .outerjoin(models.Shipping, models.Customer.customer_id == models.Shipping.customer_id)
        .all()
    )
    return results
    
