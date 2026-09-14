export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface User {
  employee_id: number;
  username: string;
  full_name: string;
  email?: string | null;
  role_id: number;
  organization_unit_id?: number | null;
  designation?: string | null;
  is_active: boolean;
}