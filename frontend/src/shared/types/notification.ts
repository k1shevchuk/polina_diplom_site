export type NotificationType =
  | "NEW_ORDER"
  | "NEW_MESSAGE"
  | "PRODUCT_APPROVED"
  | "PRODUCT_REJECTED"
  | "NEW_REVIEW";

export interface NotificationItem {
  id: number;
  user_id: number;
  type: NotificationType;
  payload_json: Record<string, unknown>;
  is_read: boolean;
  created_at: string;
}

