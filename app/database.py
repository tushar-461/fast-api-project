from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# connect_args needed for sqlite to allow multithreading
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    # import models so that they are registered on the metadata
    from . import models
    Base.metadata.create_all(bind=engine)

    # populate with sample data if empty
    from .crud import get_orders_count, create_customer, create_order
    if get_orders_count() == 0:
        # attempt to load sample data from CSV (Programiz link)
        import csv
        sample_file = os.path.join(os.path.dirname(__file__), "..", "data", "programiz_sample.csv")
        if os.path.exists(sample_file):
            with open(sample_file, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    cust = {"name": row["name"], "age": int(row["age"]), "country": row["country"]}
                    create_customer(cust)
                    order = {"item": row["item"], "amount": int(row["amount"]),
                             "shipping_status": row["shipping_status"], "customer_name": row["name"]}
                    create_order(order)
        else:
            # fallback hardcoded data
            customers = [
                {"name": "Alice", "age": 30, "country": "USA"},
                {"name": "Bob", "age": 24, "country": "Canada"},
                {"name": "Carlos", "age": 28, "country": "Spain"},
            ]
            orders = [
                {"item": "Book", "amount": 3, "shipping_status": "Delivered", "customer_name": "Alice"},
                {"item": "Laptop", "amount": 1, "shipping_status": "Shipped", "customer_name": "Bob"},
                {"item": "Pen", "amount": 10, "shipping_status": "Processing", "customer_name": "Carlos"},
            ]
            for cust in customers:
                create_customer(cust)
            for ord in orders:
                create_order(ord)

