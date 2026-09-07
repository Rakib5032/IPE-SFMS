from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.organization import OrganizationUnit


def get_organization_unit(
    db: Session,
    organization_unit_id: int,
) -> OrganizationUnit | None:
    return db.scalar(
        select(OrganizationUnit).where(
            OrganizationUnit.id == organization_unit_id
        )
    )


def get_organization_units(
    db: Session,
) -> list[OrganizationUnit]:
    return list(
        db.scalars(
            select(OrganizationUnit).order_by(
                OrganizationUnit.id
            )
        ).all()
    )


def get_group_units(
    db: Session,
    group_id: int,
) -> list[OrganizationUnit]:
    return list(
        db.scalars(
            select(OrganizationUnit)
            .where(
                (OrganizationUnit.id == group_id)
                | (
                    OrganizationUnit.parent_id
                    == group_id
                )
            )
            .order_by(OrganizationUnit.id)
        ).all()
    )


def create_organization_unit(
    db: Session,
    name: str,
    code: str,
    unit_type: str,
    parent_id: int | None = None,
    is_active: bool = True,
) -> OrganizationUnit:
    organization_unit = OrganizationUnit(
        name=name,
        code=code,
        unit_type=unit_type,
        parent_id=parent_id,
        is_active=is_active,
    )

    db.add(organization_unit)
    db.commit()
    db.refresh(organization_unit)

    return organization_unit


def update_organization_unit(
    db: Session,
    organization_unit: OrganizationUnit,
    update_data: dict,
) -> OrganizationUnit:
    for field, value in update_data.items():
        setattr(
            organization_unit,
            field,
            value,
        )

    db.commit()
    db.refresh(organization_unit)

    return organization_unit