import { beforeEach, describe, expect, it, vi } from "vitest";
import { createPinia, setActivePinia } from "pinia";

import { useNotificationsStore } from "./store";

const postMock = vi.fn(async () => ({ data: {} }));

vi.mock("../../shared/api/client", () => ({
  api: {
    get: vi.fn(async () => ({
      data: [{ id: 1, user_id: 1, type: "NEW_ORDER", payload_json: {}, is_read: false, created_at: "2026-01-01" }],
    })),
    post: (...args: any[]) => postMock(...args),
  },
}));

describe("notifications store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    postMock.mockClear();
  });

  it("marks notification as read optimistically", async () => {
    const store = useNotificationsStore();
    await store.fetchNotifications();

    await store.markAsRead(1);
    expect(store.items[0].is_read).toBe(true);
  });

  it("reverts optimistic state on error", async () => {
    postMock.mockRejectedValueOnce(new Error("network"));
    const store = useNotificationsStore();
    await store.fetchNotifications();

    await expect(store.markAsRead(1)).rejects.toThrow("network");
    expect(store.items[0].is_read).toBe(false);
  });
});
