import api from "./api";
import type {
  Layout,
  LayoutCreate,
  LayoutUpdate,
  LayoutMachine,
  LayoutMachineCreate,
  LayoutMachineUpdate,
} from "../types/layout";

export async function getLineLayouts(lineId: number): Promise<Layout[]> {
  const response = await api.get<Layout[]>(`/layouts/line/${lineId}`);
  return response.data;
}

export async function getActiveLayout(lineId: number): Promise<Layout | null> {
  const response = await api.get<Layout | null>(
    `/layouts/line/${lineId}/active`,
  );
  return response.data;
}

export async function getLayout(layoutId: number): Promise<Layout> {
  const response = await api.get<Layout>(`/layouts/${layoutId}`);
  return response.data;
}

export async function createLayout(data: LayoutCreate): Promise<Layout> {
  const response = await api.post<Layout>("/layouts/", data);
  return response.data;
}

export async function updateLayout(
  layoutId: number,
  data: LayoutUpdate,
): Promise<Layout> {
  const response = await api.put<Layout>(`/layouts/${layoutId}`, data);
  return response.data;
}

export async function completeLayout(layoutId: number): Promise<Layout> {
  const response = await api.post<Layout>(
    `/layouts/${layoutId}/complete`,
  );
  return response.data;
}

export async function getLayoutMachines(
  layoutId: number,
): Promise<LayoutMachine[]> {
  const response = await api.get<LayoutMachine[]>(
    `/layout-machines/layout/${layoutId}`,
  );
  return response.data;
}

export async function createLayoutMachine(
  data: LayoutMachineCreate,
): Promise<LayoutMachine> {
  const response = await api.post<LayoutMachine>(
    "/layout-machines/",
    data,
  );
  return response.data;
}

export async function updateLayoutMachine(
  machineId: number,
  data: LayoutMachineUpdate,
): Promise<LayoutMachine> {
  const response = await api.put<LayoutMachine>(
    `/layout-machines/${machineId}`,
    data,
  );
  return response.data;
}
