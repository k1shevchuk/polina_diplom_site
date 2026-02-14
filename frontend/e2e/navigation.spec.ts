import { expect, test, type Page } from "@playwright/test";

async function expectMainNotEmpty(page: Page) {
  const main = page.locator("main");
  await expect(main).toBeVisible();
  const text = await main.innerText();
  expect(text.trim().length).toBeGreaterThan(0);
}

test("navigation Home -> Catalog -> Product -> Cart -> About does not render empty body", async ({ page }) => {
  await page.goto("/");
  await expectMainNotEmpty(page);
  await expect(page.getByText("Craft With Love")).toBeVisible();

  await page.goto("/catalog");
  await expectMainNotEmpty(page);
  await expect(page.getByRole("heading", { level: 1 })).toContainText(/Каталог/i);

  await page.goto("/product/1");
  await expectMainNotEmpty(page);

  await page.goto("/cart");
  await expectMainNotEmpty(page);
  await expect(page.getByRole("heading", { level: 1 })).toContainText(/Вход|Корзина/i);

  await page.goto("/about");
  await expectMainNotEmpty(page);
  await expect(page.getByRole("heading", { level: 1 })).toContainText(/О бренде/i);
});
