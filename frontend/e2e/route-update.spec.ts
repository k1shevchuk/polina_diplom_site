import { expect, test } from "@playwright/test";

test("product route param update changes content without page reload", async ({ page }) => {
  await page.goto("/product/1");

  const title = page.getByRole("heading", { level: 1 });
  await expect(title).toBeVisible();

  const firstTitle = await title.innerText();
  const initialNavigationEntries = await page.evaluate(() => performance.getEntriesByType("navigation").length);

  await page.evaluate(() => {
    history.pushState({}, "", "/product/2");
    window.dispatchEvent(new PopStateEvent("popstate"));
  });

  await page.waitForURL(/\/product\/2$/);
  await expect(title).not.toHaveText(firstTitle);

  const afterNavigationEntries = await page.evaluate(() => performance.getEntriesByType("navigation").length);
  expect(afterNavigationEntries).toBe(initialNavigationEntries);
});
