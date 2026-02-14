import { expect, test } from "@playwright/test";

test("home link is not active on /catalog, catalog link is active", async ({ page }) => {
  await page.goto("/catalog");

  const homeLink = page.getByRole("link", { name: "Главная" }).first();
  const catalogLink = page.getByRole("link", { name: "Каталог" }).first();

  await expect(homeLink).toBeVisible();
  await expect(catalogLink).toBeVisible();
  await expect(homeLink).not.toHaveClass(/router-link-exact-active/);
  await expect(catalogLink).toHaveClass(/router-link-exact-active/);
});

test("home link is active on /", async ({ page }) => {
  await page.goto("/");
  const homeLink = page.getByRole("link", { name: "Главная" }).first();
  await expect(homeLink).toHaveClass(/router-link-exact-active/);
});
