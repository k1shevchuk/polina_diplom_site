import { expect, test } from "@playwright/test";

test("home page has proper brand text and no replacement symbols", async ({ page }) => {
  await page.goto("/");

  const brandLink = page.getByRole("banner").getByRole("link", { name: /Craft With Love/i }).first();
  await expect(brandLink).toBeVisible();
  await expect(page.getByRole("heading", { level: 1, name: /Связано с любовью/i })).toBeVisible();

  const bodyText = await page.locator("body").innerText();
  expect(bodyText.includes("\uFFFD")).toBe(false);
});
