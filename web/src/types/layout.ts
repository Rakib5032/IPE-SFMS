export interface Layout {
  id: number;
  line_id: number;
  style?: string | null;
  job?: string | null;
  buyer: string;
  smv: number;
  required_machine_count?: number | null;
  total_machines: number;
  machine_status: Record<string, string>;
  status: string;
  started_at: string;
  completed_at?: string | null;
  duration_minutes?: number | null;
  is_active?: boolean | null;
  notes?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface LayoutCreate {
  line_id: number;
  style?: string | null;
  job?: string | null;
  buyer: string;
  smv: number;
  required_machine_count?: number | null;
  total_machines: number;
  machine_status: Record<string, string>;
  status?: string;
  notes?: string | null;
}

export interface LayoutUpdate {
  style?: string | null;
  job?: string | null;
  buyer?: string | null;
  smv?: number | null;
  required_machine_count?: number | null;
  total_machines?: number | null;
  machine_status?: Record<string, string> | null;
  status?: string | null;
  notes?: string | null;
}

export interface LayoutMachine {
  id: number;
  layout_id: number;
  machine_number: number;
  machine_name?: string | null;
  status: string;
  reason?: string | null;
  is_active: boolean;
  started_at?: string | null;
  completed_at?: string | null;
}

export interface LayoutMachineCreate {
  layout_id: number;
  machine_number: number;
  machine_name?: string | null;
  status?: string;
  reason?: string | null;
}

export interface LayoutMachineUpdate {
  machine_name?: string | null;
  status?: string | null;
  reason?: string | null;
  is_active?: boolean | null;
}