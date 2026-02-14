export interface SellerProductFormState {
  title: string;
  description: string;
  price: string;
  stock: string;
  tags: string;
  materials: string;
  categoryId: string;
}

export interface SellerProductPayload {
  title: string;
  description: string;
  price: number;
  stock: number | null;
  category_id?: number;
  tags: string[];
  materials: string[];
  image_urls: string[];
}

export function splitCsv(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

export function normalizeStock(value: string): number | null {
  const trimmed = value.trim();
  if (!trimmed) return null;
  const numeric = Number(trimmed);
  if (!Number.isFinite(numeric)) return null;
  return Math.max(0, Math.floor(numeric));
}

export function buildSellerProductPayload(
  form: SellerProductFormState,
  imageUrls: string[],
): SellerProductPayload {
  const payload: SellerProductPayload = {
    title: form.title.trim(),
    description: form.description.trim(),
    price: Number(form.price),
    stock: normalizeStock(form.stock),
    tags: splitCsv(form.tags),
    materials: splitCsv(form.materials),
    image_urls: [...imageUrls],
  };

  const categoryId = Number(form.categoryId);
  if (Number.isFinite(categoryId) && categoryId > 0) {
    payload.category_id = categoryId;
  }

  return payload;
}
