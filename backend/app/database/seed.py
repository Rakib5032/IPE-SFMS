from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models.role import Role


ROLES = [
    {
        "name": "Administrator",
        "code": "ADMIN",
        "description": "Full system access",
    },
    {
        "name": "Deputy General Manager",
        "code": "DGM",
        "description": "Deputy General Manager",
    },
    {
        "name": "Central Manager",
        "code": "CENTRAL_MANAGER",
        "description": "Central Manager",
    },
    {
        "name": "Group Manager",
        "code": "GROUP_MANAGER",
        "description": "Group-level management access",
    },
    {
        "name": "Floor IE",
        "code": "FLOOR_IE",
        "description": "Unit-level operational access",
    },
    {
        "name": "Supervisor",
        "code": "SUPERVISOR",
        "description": "Line-level operational access",
    },
    {
        "name": "Deputy Production Manager",
        "code": "DPM",
        "description": "Unit-level operational access",
    },
    {
        "name": "Assistant Production Manager",
        "code": "APM",
        "description": "Unit-level operational access",
    },
    {
        "name": "In-Charge",
        "code": "IN_CHARGE",
        "description": "Unit-level operational access",
    },
]


def seed_roles():
    db = SessionLocal()

    try:
        for role_data in ROLES:
            existing_role = db.scalar(
                select(Role).where(
                    Role.code == role_data["code"]
                )
            )

            if existing_role:
                continue

            role = Role(**role_data)
            db.add(role)

        db.commit()

        print("Roles seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()