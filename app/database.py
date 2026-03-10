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
    from .crud import get_orders_count, create_customer, create_order, create_shipping
    if get_orders_count() == 0:
        # attempt to load sample data from CSV (Programiz link)
        import csv
        sample_file = os.path.join(os.path.dirname(__file__), "..", "data", "programiz_sample.csv")
        if os.path.exists(sample_file):
            with open(sample_file, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # split name into first/last
                    parts = row.get("name", "").split()
                    first = parts[0] if parts else ""
                    last = parts[1] if len(parts) > 1 else ""
                    cust = {"first_name": first, "last_name": last, "age": int(row["age"]), "country": row["country"]}
                    created = create_customer(cust)
                    order = {"item": row["item"], "amount": int(row["amount"]), "customer_id": created.customer_id}
                    create_order(order)
                    # optionally create shipping row for this customer
                    shipping = {"status": row.get("shipping_status", ""), "customer_id": created.customer_id}
                    create_shipping(shipping)
        else:
            # fallback hardcoded data
            sample = [
                {"first_name": "Alice", "last_name": "Smith", "age": 30, "country": "USA", "item": "Book", "amount": 3, "shipping_status": "Delivered"},
                {"first_name": "Bob", "last_name": "Jones", "age": 24, "country": "Canada", "item": "Laptop", "amount": 1, "shipping_status": "Shipped"},
                {"first_name": "Carlos", "last_name": "Reyes", "age": 28, "country": "Spain", "item": "Pen", "amount": 10, "shipping_status": "Processing"},
            ]
            for entry in sample:
                cust = {"first_name": entry["first_name"], "last_name": entry["last_name"], "age": entry["age"], "country": entry["country"]}
                created = create_customer(cust)
                create_order({"item": entry["item"], "amount": entry["amount"], "customer_id": created.customer_id})
                create_shipping({"status": entry["shipping_status"], "customer_id": created.customer_id})

