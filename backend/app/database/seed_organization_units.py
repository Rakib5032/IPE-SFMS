from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models.organization import OrganizationUnit


ORGANIZATION_UNITS = [
    {
        "name": "Group1",
        "code": "GROUP1",
        "unit_type": "GROUP",
    },
    {
        "name": "Group2",
        "code": "GROUP2",
        "unit_type": "GROUP",
    },
    {
        "name": "Group3",
        "code": "GROUP3",
        "unit_type": "GROUP",
    },
    {
        "name": "Elegant1",
        "code": "ELEGANT1",
        "unit_type": "GROUP",
    },
    {
        "name": "Elegant2",
        "code": "ELEGANT2",
        "unit_type": "GROUP",
    },
]


def seed_organization_units():
    db = SessionLocal()

    try:
        for data in ORGANIZATION_UNITS:
            existing = db.scalar(
                select(OrganizationUnit).where(
                    OrganizationUnit.code == data["code"]
                )
            )

            if existing:
                print(
                    f"Already exists: {data['name']}"
                )
                continue

            organization_unit = OrganizationUnit(
                name=data["name"],
                code=data["code"],
                unit_type=data["unit_type"],
                parent_id=None,
                is_active=True,
            )

            db.add(organization_unit)

        db.commit()

        print("Organization units seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_organization_units()