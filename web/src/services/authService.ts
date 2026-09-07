import api from "./api";
import type {
  LoginRequest,
  TokenResponse,
  User,
} from "../types/auth";

export async function login(
  credentials: LoginRequest
): Promise<TokenResponse> {
  const response = await api.post<TokenResponse>(
    "/auth/login",
    credentials
  );

  return response.data;
}

export async function getCurrentUser(): Promise<User> {
  const response = await api.get<User>("/auth/me");

  return response.data;
}

export async function refreshToken(
  refresh_token: string
): Promise<TokenResponse> {
  const response = await api.post<TokenResponse>(
    "/auth/refresh",
    {
      refresh_token,
    }
  );

  return response.data;
}

export async function logout(
  refresh_token: string
): Promise<void> {
  await api.post("/auth/logout", {
    refresh_token,
  });
}