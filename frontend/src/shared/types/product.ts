export interface ProductImage {
  id: number;
  image_url: string;
  sort_order: number;
}

export type ProductStatus = "DRAFT" | "PENDING" | "ACTIVE" | "REJECTED" | "ARCHIVED";

export interface Product {
  id: number;
  seller_id: number;
  title: string;
  description: string;
  price: string;
  stock: number | null;
  category_id: number | null;
  tags: string[];
  materials: string[];
  status: ProductStatus;
  rejection_reason: string | null;
  created_at: string;
  images: ProductImage[];
}

export interface Paginated<T> {
  items: T[];
  meta: {
    page: number;
    page_size: number;
    total: number;
  };
}
