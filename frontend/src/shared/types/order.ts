export interface CartItem {
  id: number;
  product_id: number;
  qty: number;
  title: string;
  price: string;
  seller_id: number;
}

export interface Cart {
  id: number;
  user_id: number;
  items: CartItem[];
  total_amount: string;
}

export type OrderStatus = "REQUESTED" | "ACCEPTED" | "REJECTED" | "COMPLETED" | "CANCELED";

export interface OrderItem {
  id: number;
  product_id: number | null;
  product_title_snapshot: string;
  product_price_snapshot: string;
  qty: number;
  subtotal: string;
}

export interface Order {
  id: number;
  buyer_id: number;
  seller_id: number;
  status: OrderStatus;
  full_name: string;
  phone: string;
  address: string;
  comment: string | null;
  total_amount: string;
  created_at: string;
  items: OrderItem[];
}

export interface CheckoutResponse {
  orders: Order[];
  total_orders: number;
}

