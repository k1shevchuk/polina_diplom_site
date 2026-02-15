import { expect, test } from "@playwright/test";

test("desktop drag on top slider does not open product page", async ({ page }) => {
  const catalogResponse = await page.request.get("/api/v1/catalog?page=1&page_size=12&sort=popular");
  const catalogData = catalogResponse.ok() ? await catalogResponse.json() : null;
  const productsCount = catalogData?.items?.length ?? 0;

  test.skip(productsCount < 2, "Need at least 2 products to validate slider drag behavior");

  await page.goto("/");

  const slider = page.locator("section.brand-card").first().locator(".overflow-hidden").first();
  await expect(slider).toBeVisible();
  await expect(slider.locator(".brand-product-card").first()).toBeVisible();

  const box = await slider.boundingBox();
  expect(box).not.toBeNull();

  if (!box) {
    return;
  }

  const centerY = box.y + box.height / 2;
  const startX = box.x + box.width * 0.75;
  const endX = box.x + box.width * 0.2;

  await page.mouse.move(startX, centerY);
  await page.mouse.down();
  await page.mouse.move(endX, centerY, { steps: 14 });
  await page.mouse.up();

  await page.waitForTimeout(200);
  await expect(page).toHaveURL(/\/($|\?)/);
});
