from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_customers(db: Session):
    return db.query(models.Customer).all()


def get_customer_by_name(db: Session, name: str):
    return db.query(models.Customer).filter(models.Customer.name == name).first()


def create_customer(customer: dict):
    db = SessionLocal()
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
    # allow either customer_id or name lookup
    cust = None
    if order.get("customer_id"):
        cust = db.query(models.Customer).filter(models.Customer.id == order["customer_id"]).first()
    elif order.get("customer_name"):
        cust = db.query(models.Customer).filter(models.Customer.name == order["customer_name"]).first()
    if cust:
        o = models.Order(item=order["item"], amount=order["amount"], shipping_status=order["shipping_status"], customer_id=cust.id)
        db.add(o)
        db.commit()
        db.refresh(o)
        db.close()
        return o
    db.close()
    return None


def get_joined_orders(db: Session):
    # return list of orders with customer info
    results = (
        db.query(models.Customer.name, models.Customer.age, models.Customer.country,
                 models.Order.item, models.Order.amount, models.Order.shipping_status)
        .join(models.Order, models.Customer.id == models.Order.customer_id)
        .all()
    )
    return results
