import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
  withCredentials: true,
});

let accessToken: string | null = null;

export function setAccessToken(token: string | null) {
  accessToken = token;
}

api.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

let isRefreshing = false;
let pendingQueue: Array<() => void> = [];

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    const status = error.response?.status;
    const isRefreshEndpoint = typeof original?.url === "string" && original.url.includes("/auth/refresh");

    if (status === 401 && !original._retry && !isRefreshEndpoint) {
      original._retry = true;

      if (isRefreshing) {
        await new Promise<void>((resolve) => pendingQueue.push(resolve));
        return api(original);
      }

      isRefreshing = true;
      try {
        const refresh = await api.post("/auth/refresh");
        setAccessToken(refresh.data.access_token);
        pendingQueue.forEach((r) => r());
        pendingQueue = [];
        return api(original);
      } catch (refreshError) {
        setAccessToken(null);
        pendingQueue.forEach((r) => r());
        pendingQueue = [];
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  },
);

