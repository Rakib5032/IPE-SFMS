// ============================================================
// USER
// ============================================================

export interface User {
  employee_id: number;
  username: string;
  full_name: string;
  designation: string | null;
  email: string | null;
  role_id: number;
  organization_unit_id: number | null;
  is_active: boolean;
}


// ============================================================
// USER CREATE
// ============================================================

export interface UserCreate {
  employee_id: number;
  full_name: string;
  designation?: string | null;
  email?: string | null;
  password: string;
  role_id: number;
  organization_unit_id?: number | null;
}


// ============================================================
// USER UPDATE
// ============================================================

export interface UserUpdate {
  full_name?: string | null;
  designation?: string | null;
  email?: string | null;
  password?: string | null;
  role_id?: number | null;
  organization_unit_id?: number | null;
  is_active?: boolean | null;
}