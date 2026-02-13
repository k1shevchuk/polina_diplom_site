export interface CatalogQueryInput {
  q?: string;
  category_id?: number;
  min_price?: number;
  max_price?: number;
  sort?: string;
  page?: number;
}

export function buildCatalogQuery(input: CatalogQueryInput): URLSearchParams {
  const params = new URLSearchParams();
  Object.entries(input).forEach(([key, value]) => {
    if (value === undefined || value === null || value === "") return;
    params.set(key, String(value));
  });
  return params;
}
