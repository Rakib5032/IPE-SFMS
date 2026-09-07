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

api.interceptors.request.use((config) => {
  const accessToken = getAccessToken();

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status !== 401 ||
      originalRequest?._retry
    ) {
      return Promise.reject(error);
    }

    const refreshToken = getRefreshToken();

    if (!refreshToken) {
      clearTokens();
      window.location.href = "/";
      return Promise.reject(error);
    }

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

      setTokens(
        access_token,
        refresh_token
      );

      originalRequest.headers.Authorization =
        `Bearer ${access_token}`;

      return api(originalRequest);
    } catch {
      clearTokens();
      window.location.href = "/";

      return Promise.reject(error);
    }
  }
);

export default api;