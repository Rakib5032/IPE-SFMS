import api from "./api";
import type {
  User,
  UserCreate,
  UserUpdate,
} from "../types/user";

export async function getUserByEmployeeId(
  employeeId: number
): Promise<User> {
  const response = await api.get<User>(
    `/users/${employeeId}`
  );

  return response.data;
}

export async function createUser(
  userData: UserCreate
): Promise<User> {
  const response = await api.post<User>(
    "/users/",
    userData
  );

  return response.data;
}

export async function updateUser(
  employeeId: number,
  userData: UserUpdate
): Promise<User> {
  const response = await api.patch<User>(
    `/users/${employeeId}`,
    userData
  );

  return response.data;
}