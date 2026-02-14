import { beforeEach, describe, expect, it, vi } from "vitest";
import { createPinia, setActivePinia } from "pinia";

import { useAuthStore } from "../../app/stores/auth";

const { postMock, getMock, setAccessTokenMock } = vi.hoisted(() => ({
  postMock: vi.fn(async (url: string) => {
    if (url === "/auth/login") {
      return { data: { access_token: "token123", token_type: "bearer" } };
    }
    if (url === "/auth/refresh") {
      return { data: { access_token: "token456", token_type: "bearer" } };
    }
    return { data: {} };
  }),
  getMock: vi.fn(async () => ({
    data: { id: 1, email: "user@example.com", roles: ["BUYER"], is_banned: false, is_active: true },
  })),
  setAccessTokenMock: vi.fn(),
}));

vi.mock("../../shared/api/client", () => ({
  api: {
    post: postMock,
    get: getMock,
  },
  setAccessToken: setAccessTokenMock,
}));

describe("auth store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    postMock.mockClear();
    getMock.mockClear();
    setAccessTokenMock.mockClear();
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

  it("clears local auth state on logout even when API logout fails", async () => {
    const store = useAuthStore();
    await store.login("user@example.com", "StrongPass123");

    postMock.mockImplementationOnce(async (url: string) => {
      if (url === "/auth/logout") {
        throw new Error("session already expired");
      }
      return { data: {} };
    });

    await expect(store.logout()).resolves.toBeUndefined();

    expect(store.token).toBeNull();
    expect(store.me).toBeNull();
    expect(store.isAuthenticated).toBe(false);
  });
});
