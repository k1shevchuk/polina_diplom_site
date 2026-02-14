import { expect, test, type Page } from "@playwright/test";

async function expectMainNotEmpty(page: Page) {
  const main = page.locator("main");
  await expect(main).toBeVisible();
  await expect
    .poll(async () => {
      const text = await main.innerText();
      return text.trim().length;
    })
    .toBeGreaterThan(0);
}

test("navigation Home -> Catalog -> Product -> Cart -> About does not render empty body", async ({ page }) => {
  const catalogResponse = await page.request.get("/api/v1/catalog?page=1&page_size=1&sort=new");
  const catalogData = catalogResponse.ok() ? await catalogResponse.json() : null;
  const firstProductId = catalogData?.items?.[0]?.id;

  await page.goto("/");
  await expectMainNotEmpty(page);
  const brandLink = page.getByRole("banner").getByRole("link", { name: /Craft With Love/i }).first();
  await expect(brandLink).toBeVisible();

  await page.goto("/catalog");
  await expectMainNotEmpty(page);
  await expect(page.getByRole("heading", { level: 1 })).toContainText(/Каталог/i);

  await page.goto(firstProductId ? `/product/${firstProductId}` : "/product/1");
  await expectMainNotEmpty(page);

  await page.goto("/cart");
  await expectMainNotEmpty(page);
  await expect(page.getByRole("heading", { level: 1 })).toContainText(/Вход|Корзина/i);

  await page.goto("/about");
  await expectMainNotEmpty(page);
  await expect(page.getByRole("heading", { level: 1 })).toContainText(/О бренде/i);
});
