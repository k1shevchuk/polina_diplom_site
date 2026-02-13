import { beforeEach, describe, expect, it, vi } from "vitest";
import { createPinia, setActivePinia } from "pinia";

import { useAuthStore } from "../../app/stores/auth";

vi.mock("../../shared/api/client", () => ({
  api: {
    post: vi.fn(async (url: string) => {
      if (url === "/auth/login") {
        return { data: { access_token: "token123", token_type: "bearer" } };
      }
      if (url === "/auth/refresh") {
        return { data: { access_token: "token456", token_type: "bearer" } };
      }
      return { data: {} };
    }),
    get: vi.fn(async () => ({
      data: { id: 1, email: "user@example.com", roles: ["BUYER"], is_banned: false, is_active: true },
    })),
  },
  setAccessToken: vi.fn(),
}));

describe("auth store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("stores access token and fetches me after login", async () => {
    const store = useAuthStore();
    await store.login("user@example.com", "StrongPass123");

    expect(store.token).toBe("token123");
    expect(store.me?.email).toBe("user@example.com");
    expect(store.isAuthenticated).toBe(true);
  });

  it("refresh updates access token", async () => {
    const store = useAuthStore();
    await store.refresh();
    expect(store.token).toBe("token456");
  });
});
