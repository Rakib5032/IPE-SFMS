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
ASSISTANT_MANAGER = "ASSISTANT_MANAGER"
FLOOR_IE = "FLOOR_IE"
SUPERVISOR = "SUPERVISOR"


# ------------------------------------------------------------
# Role Groups
# ------------------------------------------------------------

# Can access and manage everything
ALL_ACCESS_ROLES = {
    ADMIN,
}


# Can see the entire factory
FACTORY_VIEW_ROLES = {
    ADMIN,
    DGM,
    CENTRAL_MANAGER,
}


# Can work within their assigned group
GROUP_ROLES = {
    GROUP_MANAGER,
    ASSISTANT_MANAGER,
}


# Can work within their assigned unit
UNIT_ROLES = {
    FLOOR_IE,
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
    """

    if role_code == ADMIN:
        return "ALL"

    if role_code in {
        DGM,
        CENTRAL_MANAGER,
    }:
        return "ALL"

    if role_code in {
        GROUP_MANAGER,
        ASSISTANT_MANAGER,
    }:
        return "GROUP"

    if role_code == FLOOR_IE:
        return "UNIT"

    if role_code == SUPERVISOR:
        return "LINE"

    return "NONE"


# ------------------------------------------------------------
# User Management Rules
# ------------------------------------------------------------

def can_manage_users(role_code: str) -> bool:
    """
    User creation/update/deactivation.

    Admin:
        Full access.

    DGM / Central Manager:
        Can update employee information according
        to the application rules.

    Others:
        No general user management.
    """

    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
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
        ASSISTANT_MANAGER,
        FLOOR_IE,
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
        ASSISTANT_MANAGER,
        FLOOR_IE,
        SUPERVISOR,
    }


def can_update_production(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        ASSISTANT_MANAGER,
        FLOOR_IE,
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
        ASSISTANT_MANAGER,
        FLOOR_IE,
        SUPERVISOR,
    }


def can_update_line_status(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        ASSISTANT_MANAGER,
        FLOOR_IE,
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
        ASSISTANT_MANAGER,
        FLOOR_IE,
        SUPERVISOR,
    }


def can_update_layout(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        ASSISTANT_MANAGER,
        FLOOR_IE,
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
        ASSISTANT_MANAGER,
        FLOOR_IE,
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
        ASSISTANT_MANAGER,
    }


def can_access_unit(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        ASSISTANT_MANAGER,
        FLOOR_IE,
    }


def can_access_line(role_code: str) -> bool:
    return role_code in {
        ADMIN,
        DGM,
        CENTRAL_MANAGER,
        GROUP_MANAGER,
        ASSISTANT_MANAGER,
        FLOOR_IE,
        SUPERVISOR,
    }