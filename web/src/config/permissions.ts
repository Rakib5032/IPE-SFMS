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
// ROLE → PERMISSIONS
// ============================================================
//
// Current SFMS frontend requirement:
//
// ADMIN
//     Full access
//
// DGM
//     Management + operational access
//     No Users
//
// CENTRAL_MANAGER
//     Management + operational access
//     View Organizations
//     No Users
//
// GROUP_MANAGER
//     Group-level operational access + reports
//     No Users
//
// FLOOR_IE
//     Unit-level operational access + reports
//
// DPM
//     Same permission level as FLOOR_IE
//     Unit-level operational access + reports
//
// APM
//     Same permission level as FLOOR_IE
//     Unit-level operational access + reports
//
// IN_CHARGE
//     Same permission level as FLOOR_IE
//     Unit-level operational access + reports
//
// SUPERVISOR
//     Line-level operational access
//     No Users
//     No Organizations
//     No Reports
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
    // "VIEW_USERS",
    // "MANAGE_USERS",

    // Organizations
    // "VIEW_ORGANIZATIONS",
    // "MANAGE_ORGANIZATIONS",

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
    // "VIEW_USERS",
    // "MANAGE_USERS",

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
    // "VIEW_USERS",
    // "MANAGE_USERS",

    // Organizations
    // Organization management is not allowed here.

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
  // IN-CHARGE
  // ==========================================================

  IN_CHARGE: [
    "VIEW_DASHBOARD",

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

    // Reports intentionally excluded
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