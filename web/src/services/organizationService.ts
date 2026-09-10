import api from "./api";

import type {
  OrganizationUnit,
  OrganizationUnitCreate,
  OrganizationUnitUpdate,
} from "../types/organization";

import type {
  Line,
  LineCreate,
  LineUpdate,
} from "../types/line";


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
//
// IMPORTANT:
// Line operations use the canonical /lines API.
// ============================================================


export async function getUnitLines(
  unitId: number,
): Promise<Line[]> {
  const response =
    await api.get<Line[]>(
      "/lines/"
    );

  /*
   * The backend already applies role-based authorization.
   *
   * This filter only selects the requested unit from the
   * lines that the current user is already allowed to see.
   */
  return response.data.filter(
    (line) =>
      line.organization_unit_id === unitId
  );
}


export async function createLine(
  unitId: number,
  data: LineCreate,
): Promise<Line> {
  const payload: LineCreate = {
    ...data,
    organization_unit_id: unitId,
  };

  const response =
    await api.post<Line>(
      "/lines/",
      payload,
    );

  return response.data;
}


export async function updateLine(
  lineId: number,
  data: LineUpdate,
): Promise<Line> {
  const response =
    await api.put<Line>(
      `/lines/${lineId}`,
      data,
    );

  return response.data;
}