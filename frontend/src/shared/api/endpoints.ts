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
  seller: {
    products: "/seller/products",
    dashboard: "/seller/dashboard",
    profile: "/seller/profile",
    uploadImage: "/seller/products/upload-image",
    publicById: (sellerId: number) => `/sellers/${sellerId}`,
  },
  admin: {
    users: "/admin/users",
    products: "/admin/products",
    reviews: "/admin/reviews",
    stats: "/admin/stats",
    statsTrend: "/admin/stats/trend",
    audit: "/admin/audit",
  },
  favorites: "/favorites",
  reviewsByProduct: (productId: number) => `/reviews/product/${productId}`,
  messages: {
    conversations: "/messages/conversations",
  },
  notifications: "/notifications",
};

