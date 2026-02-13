import { beforeEach, describe, expect, it, vi } from "vitest";
import { createPinia, setActivePinia } from "pinia";

import { useAuthStore } from "../stores/auth";
import { authGuard } from "./guards";

describe("router auth guard", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("redirects guest to login for protected route", async () => {
    const next = vi.fn();
    await authGuard({ meta: {} } as any, {} as any, next);
    expect(next).toHaveBeenCalledWith("/auth/login");
  });

  it("allows user with required role", async () => {
    const auth = useAuthStore();
    auth.token = "token";
    auth.me = { id: 1, email: "u@u.com", roles: ["SELLER"], is_banned: false, is_active: true };

    const next = vi.fn();
    await authGuard({ meta: { roles: ["SELLER"] } } as any, {} as any, next);
    expect(next).toHaveBeenCalledWith();
  });

  it("redirects when missing role", async () => {
    const auth = useAuthStore();
    auth.token = "token";
    auth.me = { id: 1, email: "u@u.com", roles: ["BUYER"], is_banned: false, is_active: true };

    const next = vi.fn();
    await authGuard({ meta: { roles: ["ADMIN"] } } as any, {} as any, next);
    expect(next).toHaveBeenCalledWith("/");
  });
});

