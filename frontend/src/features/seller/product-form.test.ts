import { describe, expect, it } from "vitest";

import { buildSellerProductPayload, normalizeStock, splitCsv } from "./product-form";

describe("seller product form helpers", () => {
  it("normalizes stock values safely", () => {
    expect(normalizeStock("")).toBeNull();
    expect(normalizeStock("12")).toBe(12);
    expect(normalizeStock("-4")).toBe(0);
    expect(normalizeStock("foo")).toBeNull();
  });

  it("splits csv values and trims empty parts", () => {
    expect(splitCsv(" wool, cotton , , soft ")).toEqual(["wool", "cotton", "soft"]);
  });

  it("builds payload for API with nullable stock and image urls", () => {
    const payload = buildSellerProductPayload(
      {
        title: " Cozy scarf ",
        description: " Warm scarf for winter mornings ",
        price: "2100",
        stock: "",
        tags: "scarf, winter",
        materials: "wool, cotton",
        categoryId: "3",
      },
      ["/media/products/a.jpg", "/media/products/b.jpg"],
    );

    expect(payload).toEqual({
      title: "Cozy scarf",
      description: "Warm scarf for winter mornings",
      price: 2100,
      stock: null,
      category_id: 3,
      tags: ["scarf", "winter"],
      materials: ["wool", "cotton"],
      image_urls: ["/media/products/a.jpg", "/media/products/b.jpg"],
    });
  });
});
