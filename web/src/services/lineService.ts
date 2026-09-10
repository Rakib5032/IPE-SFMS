import api from "./api";

import type {
  Line,
  LineCreate,
  LineUpdate,
} from "../types/line";

export async function getLines(): Promise<Line[]> {
  const response = await api.get<Line[]>(
    "/lines/"
  );

  return response.data;
}

export async function getLine(
  lineId: number
): Promise<Line> {
  const response = await api.get<Line>(
    `/lines/${lineId}`
  );

  return response.data;
}

export async function createLine(
  lineData: LineCreate
): Promise<Line> {
  const response = await api.post<Line>(
    "/lines/",
    lineData
  );

  return response.data;
}

export async function updateLine(
  lineId: number,
  lineData: LineUpdate
): Promise<Line> {
  const response = await api.put<Line>(
    `/lines/${lineId}`,
    lineData
  );

  return response.data;
}