// ============================================================
// SFMS ROLE & PERMISSION CONFIGURATION
// ============================================================
//
// Role IDs are taken from the current database:
//
// 1  → ADMIN
// 2  → DGM
// 3  → CENTRAL_MANAGER
// 4  → GROUP_MANAGER
// 5  → FLOOR_IE
// 6  → SUPERVISOR
// 8  → DPM
// 9  → APM
// 10 → IN_CHARGE
//
// The frontend uses role_id for UI access control.
// The backend remains the final authority for security.
//
// IMPORTANT
// ------------------------------------------------------------
// This file defines BASE ROLE permissions.
//
// Organization editing is NOT automatically granted to
// DGM, CENTRAL_MANAGER, or GROUP_MANAGER.
//
// An Administrator may later grant organization-edit access
// to an individual eligible manager through user-specific
// permission overrides.
// ============================================================


// ============================================================
// ROLE CODES
// ============================================================

export type RoleCode =
  | "ADMIN"
  | "DGM"
  | "CENTRAL_MANAGER"
  | "GROUP_MANAGER"
  | "FLOOR_IE"
  | "DPM"
  | "APM"
  | "IN_CHARGE"
  | "SUPERVISOR";


// ============================================================
// PERMISSIONS
// ============================================================

export type Permission =
  | "VIEW_DASHBOARD"

  // Users
  | "VIEW_USERS"
  | "MANAGE_USERS"

  // Organizations
  | "VIEW_ORGANIZATIONS"
  | "MANAGE_ORGANIZATIONS"

  // Lines
  | "VIEW_LINES"
  | "MANAGE_LINES"
  | "ASSIGN_LINES"

  // Layout
  | "VIEW_LAYOUT"
  | "MANAGE_LAYOUT"

  // Production
  | "VIEW_PRODUCTION"
  | "MANAGE_PRODUCTION"

  // Line status
  | "VIEW_LINE_STATUS"
  | "MANAGE_LINE_STATUS"

  // Reports
  | "VIEW_REPORTS";


// ============================================================
// ROLE ID → ROLE CODE
// ============================================================

const roleCodes: Record<number, RoleCode> = {
  1: "ADMIN",
  2: "DGM",
  3: "CENTRAL_MANAGER",
  4: "GROUP_MANAGER",
  5: "FLOOR_IE",
  6: "SUPERVISOR",
  8: "DPM",
  9: "APM",
  10: "IN_CHARGE",
};


// ============================================================
// ROLE → BASE PERMISSIONS
// ============================================================
//
// ORGANIZATION ACCESS
//
// ADMIN
//     View all organizations.
//     Manage organizations.
//
// DGM
//     View organizations.
//     Organization editing is NOT granted by default.
//
// CENTRAL_MANAGER
//     View organizations.
//     Organization editing is NOT granted by default.
//
// GROUP_MANAGER
//     View assigned group and its units.
//     Organization editing is NOT granted by default.
//
// FLOOR_IE
//     No Organization page.
//     Works through Lines for assigned unit.
//
// DPM
//     No Organization page.
//     Works through Lines for assigned unit.
//
// APM
//     No Organization page.
//     Works through Lines for assigned unit.
//
// IN_CHARGE
//     No Organization page.
//     Works through Lines for assigned unit.
//
// SUPERVISOR
//     No Organization page.
//     Works through assigned line(s) only.
//
// ============================================================

const rolePermissions: Record<
  RoleCode,
  Permission[]
> = {

  // ==========================================================
  // ADMINISTRATOR
  // ==========================================================

  ADMIN: [
    "VIEW_DASHBOARD",

    // Users
    "VIEW_USERS",
    "MANAGE_USERS",

    // Organizations
    "VIEW_ORGANIZATIONS",
    "MANAGE_ORGANIZATIONS",

    // Lines
    "VIEW_LINES",
    "MANAGE_LINES",
    "ASSIGN_LINES",

    // Layout
    "VIEW_LAYOUT",
    "MANAGE_LAYOUT",

    // Production
    "VIEW_PRODUCTION",
    "MANAGE_PRODUCTION",

    // Line status
    "VIEW_LINE_STATUS",
    "MANAGE_LINE_STATUS",

    // Reports
    "VIEW_REPORTS",
  ],


  // ==========================================================
  // DEPUTY GENERAL MANAGER
  // ==========================================================

  DGM: [
    "VIEW_DASHBOARD",

    // Users
    // No user management access.

    // Organizations
    "VIEW_ORGANIZATIONS",

    // Lines
    "VIEW_LINES",
    "MANAGE_LINES",
    "ASSIGN_LINES",

    // Layout
    "VIEW_LAYOUT",
    "MANAGE_LAYOUT",

    // Production
    "VIEW_PRODUCTION",
    "MANAGE_PRODUCTION",

    // Line status
    "VIEW_LINE_STATUS",
    "MANAGE_LINE_STATUS",

    // Reports
    "VIEW_REPORTS",
  ],


  // ==========================================================
  // CENTRAL MANAGER
  // ==========================================================

  CENTRAL_MANAGER: [
    "VIEW_DASHBOARD",

    // Users
    // No user management access.

    // Organizations
    "VIEW_ORGANIZATIONS",

    // Lines
    "VIEW_LINES",
    "MANAGE_LINES",
    "ASSIGN_LINES",

    // Layout
    "VIEW_LAYOUT",
    "MANAGE_LAYOUT",

    // Production
    "VIEW_PRODUCTION",
    "MANAGE_PRODUCTION",

    // Line status
    "VIEW_LINE_STATUS",
    "MANAGE_LINE_STATUS",

    // Reports
    "VIEW_REPORTS",
  ],


  // ==========================================================
  // GROUP MANAGER
  // ==========================================================

  GROUP_MANAGER: [
    "VIEW_DASHBOARD",

    // Users
    // No user management access.

    // Organizations
    // View assigned group only.
    "VIEW_ORGANIZATIONS",

    // Lines
    "VIEW_LINES",
    "ASSIGN_LINES",

    // Layout
    "VIEW_LAYOUT",
    "MANAGE_LAYOUT",

    // Production
    "VIEW_PRODUCTION",
    "MANAGE_PRODUCTION",

    // Line status
    "VIEW_LINE_STATUS",
    "MANAGE_LINE_STATUS",

    // Reports
    "VIEW_REPORTS",
  ],


  // ==========================================================
  // FLOOR IE
  // ==========================================================

  FLOOR_IE: [
    "VIEW_DASHBOARD",

    // No Organization page.
    // Access assigned unit through Lines.

    // Lines
    "VIEW_LINES",
    "ASSIGN_LINES",

    // Layout
    "VIEW_LAYOUT",
    "MANAGE_LAYOUT",

    // Production
    "VIEW_PRODUCTION",
    "MANAGE_PRODUCTION",

    // Line status
    "VIEW_LINE_STATUS",
    "MANAGE_LINE_STATUS",

    // Reports
    "VIEW_REPORTS",
  ],


  // ==========================================================
  // DEPUTY PRODUCTION MANAGER
  // ==========================================================

  DPM: [
    "VIEW_DASHBOARD",

    // No Organization page.
    // Access assigned unit through Lines.

    // Lines
    "VIEW_LINES",
    "ASSIGN_LINES",

    // Layout
    "VIEW_LAYOUT",
    "MANAGE_LAYOUT",

    // Production
    "VIEW_PRODUCTION",
    "MANAGE_PRODUCTION",

    // Line status
    "VIEW_LINE_STATUS",
    "MANAGE_LINE_STATUS",

    // Reports
    "VIEW_REPORTS",
  ],


  // ==========================================================
  // ASSISTANT PRODUCTION MANAGER
  // ==========================================================

  APM: [
    "VIEW_DASHBOARD",

    // No Organization page.
    // Access assigned unit through Lines.

    // Layout
    "VIEW_LAYOUT",
    "MANAGE_LAYOUT",

    // Production
    "VIEW_PRODUCTION",
    "MANAGE_PRODUCTION",

    // Line status
    "VIEW_LINE_STATUS",
    "MANAGE_LINE_STATUS",

    // Lines
    "VIEW_LINES",
    "ASSIGN_LINES",

    // Reports
    "VIEW_REPORTS",
  ],


  // ==========================================================
  // IN-CHARGE
  // ==========================================================

  IN_CHARGE: [
    "VIEW_DASHBOARD",

    // No Organization page.
    // Access assigned unit through Lines.

    // Lines
    "VIEW_LINES",
    "ASSIGN_LINES",

    // Layout
    "VIEW_LAYOUT",
    "MANAGE_LAYOUT",

    // Production
    "VIEW_PRODUCTION",
    "MANAGE_PRODUCTION",

    // Line status
    "VIEW_LINE_STATUS",
    "MANAGE_LINE_STATUS",

    // Reports
    "VIEW_REPORTS",
  ],


  // ==========================================================
  // SUPERVISOR
  // ==========================================================

  SUPERVISOR: [
    "VIEW_DASHBOARD",

    // No Organization page.
    // Only assigned line(s) are accessible.

    // Lines
    "VIEW_LINES",

    // Layout
    "VIEW_LAYOUT",
    "MANAGE_LAYOUT",

    // Production
    "VIEW_PRODUCTION",
    "MANAGE_PRODUCTION",

    // Line status
    "VIEW_LINE_STATUS",
    "MANAGE_LINE_STATUS",

    // Reports intentionally excluded.
  ],
};


// ============================================================
// GET ROLE CODE
// ============================================================

export function getRoleCode(
  roleId: number | undefined,
): RoleCode | null {

  if (roleId === undefined) {
    return null;
  }

  return roleCodes[roleId] ?? null;
}


// ============================================================
// CHECK PERMISSION
// ============================================================

export function hasPermission(
  roleId: number | undefined,
  permission: Permission,
): boolean {

  const roleCode = getRoleCode(roleId);

  if (!roleCode) {
    return false;
  }

  return rolePermissions[
    roleCode
  ].includes(permission);
}


// ============================================================
// GET ALL PERMISSIONS FOR A ROLE
// ============================================================

export function getPermissions(
  roleId: number | undefined,
): Permission[] {

  const roleCode = getRoleCode(roleId);

  if (!roleCode) {
    return [];
  }

  return rolePermissions[
    roleCode
  ];
}


// ============================================================
// CHECK ROLE
// ============================================================

export function hasRole(
  roleId: number | undefined,
  roleCode: RoleCode,
): boolean {

  return getRoleCode(roleId) === roleCode;
}