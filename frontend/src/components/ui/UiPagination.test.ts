import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import UiPagination from "./UiPagination.vue";

describe("UiPagination", () => {
  it("recalculates page count when total changes", async () => {
    const wrapper = mount(UiPagination, {
      props: {
        page: 1,
        pageSize: 12,
        total: 34,
      },
    });

    expect(wrapper.text()).toMatch(/\/\s*3/);

    await wrapper.setProps({ total: 3 });

    expect(wrapper.text()).toMatch(/\/\s*1/);
  });
});
