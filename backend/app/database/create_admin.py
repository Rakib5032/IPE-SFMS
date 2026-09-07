from getpass import getpass

from sqlalchemy import select

from app.core.security import hash_password
from app.database.connection import SessionLocal
from app.models.role import Role
from app.models.user import User


def create_admin():
    db = SessionLocal()

    try:
        admin_role = db.scalar(
            select(Role).where(Role.code == "ADMIN")
        )

        if not admin_role:
            print("ADMIN role not found.")
            return

        existing_admin = db.scalar(
            select(User).where(User.role_id == admin_role.id)
        )

        if existing_admin:
            print(
                f"Admin already exists: {existing_admin.username}"
            )
            return

        print("Create SFMS Administrator")
        print("-" * 30)

        employee_id = input("Employee ID: ").strip()
        username = input("Username: ").strip()
        full_name = input("Full name: ").strip()
        email = input("Email (optional): ").strip() or None

        password = getpass("Password: ")
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            print("Passwords do not match.")
            return

        if len(password) < 2:
            print("Password must be at least 8 characters.")
            return

        existing_employee = db.scalar(
            select(User).where(
                User.employee_id == employee_id
            )
        )

        if existing_employee:
            print("Employee ID already exists.")
            return

        existing_username = db.scalar(
            select(User).where(
                User.username == username
            )
        )

        if existing_username:
            print("Username already exists.")
            return

        if email:
            existing_email = db.scalar(
                select(User).where(
                    User.email == email
                )
            )

            if existing_email:
                print("Email already exists.")
                return

        admin = User(
            employee_id=employee_id,
            username=username,
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role_id=admin_role.id,
            organization_unit_id=None,
            is_active=True,
        )

        db.add(admin)
        db.commit()

        print()
        print("Admin account created successfully.")
        print(f"Username: {username}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()