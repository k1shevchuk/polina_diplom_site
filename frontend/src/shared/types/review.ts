export interface Review {
  id: number;
  user_id: number;
  product_id: number;
  order_item_id: number;
  rating: number;
  text: string;
  is_hidden: boolean;
  created_at: string;
}

