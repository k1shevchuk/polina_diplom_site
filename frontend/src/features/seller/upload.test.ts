import { describe, expect, it, vi } from "vitest";

import { uploadSellerImages } from "./upload";

describe("uploadSellerImages", () => {
  it("uploads files one by one and returns uploaded urls", async () => {
    const post = vi
      .fn()
      .mockResolvedValueOnce({ data: { url: "/media/products/one.jpg" } })
      .mockResolvedValueOnce({ data: { url: "/media/products/two.jpg" } });

    const fakeApi = { post } as any;
    const files = [
      new File(["aaa"], "one.jpg", { type: "image/jpeg" }),
      new File(["bbb"], "two.jpg", { type: "image/jpeg" }),
    ];

    const urls = await uploadSellerImages(fakeApi, "/seller/products/upload-image", files);

    expect(urls).toEqual(["/media/products/one.jpg", "/media/products/two.jpg"]);
    expect(post).toHaveBeenCalledTimes(2);
    expect(post).toHaveBeenNthCalledWith(
      1,
      "/seller/products/upload-image",
      expect.any(FormData),
      expect.objectContaining({ headers: { "Content-Type": "multipart/form-data" } }),
    );
  });
});
