export interface Line {
  id: number;
  line_number: number;
  name: string;
  organization_unit_id: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LineCreate {
  line_number: number;
  name: string;
  organization_unit_id: number;
  is_active?: boolean;
}

export interface LineUpdate {
  line_number?: number;
  name?: string;
  organization_unit_id?: number;
  is_active?: boolean;
}