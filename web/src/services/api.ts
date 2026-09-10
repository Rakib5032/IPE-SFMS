import axios from "axios";

import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} from "../utils/storage";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

/*
 * Add access token to normal authenticated requests.
 */
api.interceptors.request.use((config) => {
  const accessToken = getAccessToken();

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
});

/*
 * Response interceptor
 */
api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    /*
     * IMPORTANT:
     *
     * Login itself is expected to return 401 when the
     * Employee ID or password is wrong.
     *
     * DO NOT redirect/reload the page in that case.
     *
     * Let Login.tsx handle the error and show the popup.
     */
    const requestUrl = originalRequest?.url || "";

    if (
      requestUrl.includes("/auth/login") ||
      requestUrl.endsWith("/auth/login")
    ) {
      return Promise.reject(error);
    }

    /*
     * Only handle 401 errors for authenticated requests.
     */
    if (
      error.response?.status !== 401 ||
      originalRequest?._retry
    ) {
      return Promise.reject(error);
    }

    /*
     * Get refresh token.
     */
    const refreshToken = getRefreshToken();

    /*
     * No refresh token means the user is not authenticated.
     *
     * Do NOT redirect if this is already the login page/request.
     */
    if (!refreshToken) {
      clearTokens();

      if (window.location.pathname !== "/") {
        window.location.href = "/";
      }

      return Promise.reject(error);
    }

    /*
     * Prevent infinite retry loop.
     */
    originalRequest._retry = true;

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/auth/refresh",
        {
          refresh_token: refreshToken,
        }
      );

      const {
        access_token,
        refresh_token,
      } = response.data;

      /*
       * Save new tokens.
       */
      setTokens(
        access_token,
        refresh_token
      );

      /*
       * Retry original request with new token.
       */
      originalRequest.headers.Authorization =
        `Bearer ${access_token}`;

      return api(originalRequest);
    } catch (refreshError) {
      /*
       * Refresh failed.
       */
      clearTokens();

      if (window.location.pathname !== "/") {
        window.location.href = "/";
      }

      return Promise.reject(refreshError);
    }
  }
);

export default api;