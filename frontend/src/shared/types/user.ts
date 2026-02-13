export interface UserPublic {
  id: number;
  email: string;
  is_active: boolean;
  is_banned: boolean;
  roles: Array<{ id: number; name: "BUYER" | "SELLER" | "ADMIN" }>;
  created_at: string;
}
