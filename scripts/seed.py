"""Seed script for loading admin credentials"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from ums.db.base import Base
from ums.admin.auth import AdminModel
from ums.settings import settings


def seed_admin(username: str, password: str):
    DATABASE_URL = str(settings.db_url)
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(bind=engine)

    admin_data = {
        "first_name": "Dev",
        "last_name": "admin",
        "login": username,
        "password": password,
    }

    admin = AdminModel(**admin_data)
    session.add(admin)
    session.commit()


if __name__ == "__main__":
    # Check if both username and password are provided
    if len(sys.argv) != 3:
        print("Usage: python scripts/seed.py <admin> <admin@123>")
        sys.exit(1)

    username = str(sys.argv[1])
    password = str(sys.argv[2])
    if len(password) < 5:
        print("Weak password, please use a stronger password")
        sys.exit(1)

    # Seed admin data
    seed_admin(username, password)

    print("Admin data seeded successfully.")
