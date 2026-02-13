export const endpoints = {
  auth: {
    register: "/auth/register",
    login: "/auth/login",
    logout: "/auth/logout",
    refresh: "/auth/refresh",
    me: "/auth/me",
    sellerRole: "/auth/roles/seller",
  },
  catalog: "/catalog",
  cart: "/cart",
  checkout: "/orders/checkout",
  orders: {
    buyer: "/orders/my",
    seller: "/orders/seller",
  },
  favorites: "/favorites",
  reviewsByProduct: (productId: number) => `/reviews/product/${productId}`,
  messages: {
    conversations: "/messages/conversations",
  },
  notifications: "/notifications",
};
