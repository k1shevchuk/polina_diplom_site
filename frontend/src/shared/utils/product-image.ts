import type { Product } from "../types/product";

const knitwearFallbacks = [
  "/brand/products/scarf1.jpg",
  "/brand/products/mittens1.jpg",
  "/brand/products/socks1.jpg",
  "/brand/products/cardigan1.jpg",
  "/brand/products/dress1.jpg",
  "/brand/products/skirt1.jpg",
  "/brand/products/bag1.jpg",
  "/brand/products/sweater1.jpg",
];

export function getProductImage(product: Product): string {
  const first = product.images?.[0]?.image_url;
  if (first) return first;
  return knitwearFallbacks[product.id % knitwearFallbacks.length];
}
