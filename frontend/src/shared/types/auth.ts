export type RoleName = "BUYER" | "SELLER" | "ADMIN";

export interface UserMe {
  id: number;
  email: string;
  roles: RoleName[];
  is_banned: boolean;
  is_active: boolean;
}

export interface AuthTokens {
  access_token: string;
  token_type: "bearer";
}

