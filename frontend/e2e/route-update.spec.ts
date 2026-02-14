import { expect, test } from "@playwright/test";

test("product route param update changes content without page reload", async ({ page, request }) => {
  const catalogResponse = await request.get("/api/v1/catalog?page=1&page_size=2&sort=new");
  const catalogData = catalogResponse.ok() ? await catalogResponse.json() : null;
  const productIds = Array.isArray(catalogData?.items) ? catalogData.items.map((item: { id: number }) => item.id) : [];

  test.skip(productIds.length < 2, "Нужно минимум 2 товара в каталоге для проверки route update");

  const firstId = productIds[0];
  const secondId = productIds[1];

  await page.goto(`/product/${firstId}`);

  const title = page.getByRole("heading", { level: 1 });
  await expect(title).toBeVisible();

  const firstTitle = await title.innerText();
  const initialNavigationEntries = await page.evaluate(() => performance.getEntriesByType("navigation").length);

  await page.evaluate((id) => {
    history.pushState({}, "", `/product/${id}`);
    window.dispatchEvent(new PopStateEvent("popstate"));
  }, secondId);

  await page.waitForURL(new RegExp(`/product/${secondId}$`));
  await expect(title).not.toHaveText(firstTitle);

  const afterNavigationEntries = await page.evaluate(() => performance.getEntriesByType("navigation").length);
  expect(afterNavigationEntries).toBe(initialNavigationEntries);
});
