export interface Conversation {
  id: number;
  buyer_id: number;
  seller_id: number;
  product_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: number;
  conversation_id: number;
  sender_id: number;
  body: string;
  is_read: boolean;
  created_at: string;
}

