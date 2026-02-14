import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";

import { authGuard } from "./guards";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: () => import("../layouts/PublicLayout.vue"),
    children: [
      { path: "", component: () => import("../../views/public/HomeView.vue"), meta: { public: true } },
      { path: "catalog", component: () => import("../../views/public/CatalogView.vue"), meta: { public: true } },
      { path: "product/:id", component: () => import("../../views/public/ProductView.vue"), meta: { public: true } },
      { path: "seller/:id", component: () => import("../../views/public/SellerPublicView.vue"), meta: { public: true } },
      { path: "about", component: () => import("../../views/public/AboutView.vue"), meta: { public: true } },
      { path: "customers", component: () => import("../../views/public/CustomersView.vue"), meta: { public: true } },
      { path: "reviews", redirect: "/customers" },
      { path: "account", redirect: "/me" },
      { path: "auth/login", component: () => import("../../views/public/LoginView.vue"), meta: { public: true } },
      { path: "auth/register", component: () => import("../../views/public/RegisterView.vue"), meta: { public: true } },
    ],
  },
  {
    path: "/",
    component: () => import("../layouts/BuyerLayout.vue"),
    meta: { roles: ["BUYER", "SELLER", "ADMIN"] },
    children: [
      { path: "cart", component: () => import("../../views/buyer/CartView.vue") },
      { path: "checkout", component: () => import("../../views/buyer/CheckoutView.vue") },
      { path: "orders", component: () => import("../../views/buyer/OrdersView.vue") },
      { path: "orders/:id", component: () => import("../../views/buyer/OrderDetailsView.vue") },
      { path: "favorites", component: () => import("../../views/buyer/FavoritesView.vue") },
      { path: "messages", component: () => import("../../views/buyer/MessagesView.vue") },
      { path: "notifications", component: () => import("../../views/buyer/NotificationsView.vue") },
      { path: "me", component: () => import("../../views/buyer/MeView.vue") },
    ],
  },
  {
    path: "/seller",
    component: () => import("../layouts/SellerLayout.vue"),
    meta: { roles: ["SELLER", "ADMIN"] },
    children: [
      { path: "dashboard", component: () => import("../../views/seller/DashboardView.vue") },
      { path: "products", component: () => import("../../views/seller/ProductsView.vue") },
      { path: "products/new", component: () => import("../../views/seller/ProductNewView.vue") },
      { path: "products/:id/edit", component: () => import("../../views/seller/ProductEditView.vue") },
      { path: "orders", component: () => import("../../views/seller/OrdersView.vue") },
      { path: "orders/:id", component: () => import("../../views/seller/OrderDetailsView.vue") },
      { path: "messages", component: () => import("../../views/seller/MessagesView.vue") },
      { path: "notifications", component: () => import("../../views/seller/NotificationsView.vue") },
      { path: "profile", component: () => import("../../views/seller/ProfileView.vue") },
    ],
  },
  {
    path: "/admin",
    component: () => import("../layouts/AdminLayout.vue"),
    meta: { roles: ["ADMIN"] },
    children: [
      { path: "", component: () => import("../../views/admin/AdminHomeView.vue") },
      { path: "users", component: () => import("../../views/admin/UsersView.vue") },
      { path: "products", component: () => import("../../views/admin/ProductsView.vue") },
      { path: "moderation/products", component: () => import("../../views/admin/ModerationProductsView.vue") },
      { path: "reviews", component: () => import("../../views/admin/ReviewsView.vue") },
      { path: "stats", component: () => import("../../views/admin/StatsView.vue") },
      { path: "audit", component: () => import("../../views/admin/AuditView.vue") },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkActiveClass: "router-link-active",
  linkExactActiveClass: "router-link-exact-active",
  scrollBehavior(to) {
    if (to.hash) {
      return { el: to.hash, top: 96, behavior: "smooth" };
    }
    return { top: 0, behavior: "smooth" };
  },
});

router.beforeEach(authGuard);

export default router;

