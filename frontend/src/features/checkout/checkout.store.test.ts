import { beforeEach, describe, expect, it, vi } from "vitest";
import { createPinia, setActivePinia } from "pinia";

import { useCheckoutStore } from "./store";

vi.mock("../../shared/api/client", () => ({
  api: {
    post: vi.fn(async () => ({
      data: {
        orders: [
          { id: 10, seller_id: 2, total_amount: "100.00", items: [] },
          { id: 11, seller_id: 3, total_amount: "70.00", items: [] },
        ],
        total_orders: 2,
      },
    })),
  },
}));

describe("checkout store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("stores split orders response", async () => {
    const store = useCheckoutStore();

    const response = await store.checkout({
      full_name: "Test",
      phone: "+7000",
      address: "Address",
    });

    expect(response.total_orders).toBe(2);
    expect(store.lastCheckout?.orders[0].seller_id).toBe(2);
    expect(store.lastCheckout?.orders[1].seller_id).toBe(3);
  });
});
