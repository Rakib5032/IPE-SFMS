import api from "./api";

import type {
  OrganizationUnit,
  OrganizationUnitCreate,
  OrganizationUnitUpdate,
  Line,
  LineCreate,
  LineUpdate,
} from "../types/organization";


// ============================================================
// ORGANIZATION UNITS
// ============================================================

export async function getOrganizationUnits(): Promise<
  OrganizationUnit[]
> {
  const response =
    await api.get<OrganizationUnit[]>(
      "/organization/"
    );

  return response.data;
}


export async function createOrganizationUnit(
  data: OrganizationUnitCreate,
): Promise<OrganizationUnit> {
  const response =
    await api.post<OrganizationUnit>(
      "/organization/",
      data,
    );

  return response.data;
}


export async function updateOrganizationUnit(
  id: number,
  data: OrganizationUnitUpdate,
): Promise<OrganizationUnit> {
  const response =
    await api.put<OrganizationUnit>(
      `/organization/${id}`,
      data,
    );

  return response.data;
}


// ============================================================
// LINES
// ============================================================

export async function getUnitLines(
  unitId: number,
): Promise<Line[]> {
  const response =
    await api.get<Line[]>(
      `/organization/${unitId}/lines`,
    );

  return response.data;
}


export async function createLine(
  unitId: number,
  data: LineCreate,
): Promise<Line> {
  const response =
    await api.post<Line>(
      `/organization/${unitId}/lines`,
      data,
    );

  return response.data;
}


export async function updateLine(
  lineId: number,
  data: LineUpdate,
): Promise<Line> {
  const response =
    await api.put<Line>(
      `/organization/lines/${lineId}`,
      data,
    );

  return response.data;
}