# ============================================================
# SFMS - Role & Access Rules
# ============================================================


# ------------------------------------------------------------
# Role Codes
# ------------------------------------------------------------

ADMIN = "ADMIN"
DGM = "DGM"
CENTRAL_MANAGER = "CENTRAL_MANAGER"
GROUP_MANAGER = "GROUP_MANAGER"

FLOOR_IE = "FLOOR_IE"
DPM = "DPM"
APM = "APM"
IN_CHARGE = "IN_CHARGE"

SUPERVISOR = "SUPERVISOR"


# Role Groups

# Full system access
ALL_ACCESS_ROLES = {
    ADMIN,
}


# Can access the entire factory
FACTORY_VIEW_ROLES = {
    ADMIN,
    DGM,
    CENTRAL_MANAGER,
}


# Can work within their assigned group
GROUP_ROLES = {
    GROUP_MANAGER,
}


# Can work within their assigned unit
UNIT_ROLES = {
    FLOOR_IE,
    DPM,
    APM,
    IN_CHARGE,
}


# Can work only on assigned lines
LINE_ROLES = {
    SUPERVISOR,
}


# ------------------------------------------------------------
# Role Helpers
# ------------------------------------------------------------

def is_admin(role_code: str) -> bool:
    return role_code == ADMIN


def can_view_factory(role_code: str) -> bool:
    return role_code in FACTORY_VIEW_ROLES


def is_group_role(role_code: str) -> bool:
    return role_code in GROUP_ROLES


def is_unit_role(role_code: str) -> bool:
    return role_code in UNIT_ROLES


def is_line_role(role_code: str) -> bool:
    return role_code in LINE_ROLES


# ------------------------------------------------------------
# Dashboard Scope
# ------------------------------------------------------------

def get_dashboard_scope(role_code: str) -> str:
    """
    Return the scope of the dashboard for a role.

    Possible values:
        ALL
        GROUP
        UNIT
        LINE
        NONE
    """

    if role_code in ALL_ACCESS_ROLES:
        return "ALL"

    if role_code in FACTORY_VIEW_ROLES:
        return "ALL"

    if role_code in GROUP_ROLES:
        return "GROUP"

    if role_code in UNIT_ROLES:
        return "UNIT"

    if role_code in LINE_ROLES:
        return "LINE"

    return "NONE"


# ------------------------------------------------------------
# User Management Rules
# ------------------------------------------------------------

def can_manage_users(role_code: str) -> bool:
    """
    General user management permission.

    ADMIN:
        Full user management.

    DGM / Central Manager:
        Employee information management according
        to application rules.

    Others:
        No general user management.
    """

    return role_code in {
        ADMIN,
        # DGM,
        # CENTRAL_MANAGER,
    }


def can_create_user(role_code: str) -> bool:
    return role_code == ADMIN


def can_update_user(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
    }


def can_deactivate_user(role_code: str) -> bool:
    return role_code == ADMIN


# ------------------------------------------------------------
# Line Management Rules
# ------------------------------------------------------------

def can_manage_lines(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
    }


def can_assign_lines(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        FLOOR_IE,
        DPM,
        APM,
        IN_CHARGE,
    }


# ------------------------------------------------------------
# Production Rules
# ------------------------------------------------------------

def can_view_production(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        FLOOR_IE,
        DPM,
        APM,
        IN_CHARGE,
        SUPERVISOR,
    }


def can_update_production(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        FLOOR_IE,
        DPM,
        APM,
        IN_CHARGE,
        SUPERVISOR,
    }


# ------------------------------------------------------------
# Line Status Rules
# ------------------------------------------------------------

def can_view_line_status(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        FLOOR_IE,
        DPM,
        APM,
        IN_CHARGE,
        SUPERVISOR,
    }


def can_update_line_status(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        FLOOR_IE,
        DPM,
        APM,
        IN_CHARGE,
        SUPERVISOR,
    }


# ------------------------------------------------------------
# Layout Rules
# ------------------------------------------------------------

def can_view_layout(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        FLOOR_IE,
        DPM,
        APM,
        IN_CHARGE,
        SUPERVISOR,
    }


def can_update_layout(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        FLOOR_IE,
        DPM,
        APM,
        IN_CHARGE,
        SUPERVISOR,
    }


# ------------------------------------------------------------
# Report Rules
# ------------------------------------------------------------

def can_view_reports(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        FLOOR_IE,
        DPM,
        APM,
        IN_CHARGE,
        SUPERVISOR,
    }


# ------------------------------------------------------------
# Scope Rules
# ------------------------------------------------------------

def can_access_all_factory(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
    }


def can_access_group(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
    }


def can_access_unit(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        FLOOR_IE,
        DPM,
        APM,
        IN_CHARGE,
    }


def can_access_line(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        FLOOR_IE,
        DPM,
        APM,
        IN_CHARGE,
        SUPERVISOR,
    }