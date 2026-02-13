import { describe, expect, it, vi } from "vitest";

import { useDebounce } from "../../composables/useDebounce";
import { buildCatalogQuery } from "./query";

describe("catalog utils", () => {
  it("buildCatalogQuery omits empty values", () => {
    const params = buildCatalogQuery({ q: "bag", min_price: 100, max_price: undefined, sort: "new", page: 2 });
    expect(params.toString()).toContain("q=bag");
    expect(params.toString()).toContain("min_price=100");
    expect(params.toString()).toContain("sort=new");
    expect(params.toString()).toContain("page=2");
    expect(params.toString()).not.toContain("max_price");
  });

  it("debounces updates", async () => {
    vi.useFakeTimers();
    const debounced = useDebounce<string>(300);
    debounced.set("first");
    debounced.set("second");

    vi.advanceTimersByTime(299);
    expect(debounced.value.value).toBeNull();

    vi.advanceTimersByTime(1);
    expect(debounced.value.value).toBe("second");

    vi.useRealTimers();
  });
});

