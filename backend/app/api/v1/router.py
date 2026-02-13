from fastapi import APIRouter

from app.api.v1.endpoints import (
    admin_audit,
    admin_products,
    admin_reviews,
    admin_stats,
    admin_users,
    auth,
    cart,
    catalog,
    favorites,
    messages,
    notifications,
    orders,
    reviews,
    seller_dashboard,
    seller_products,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["catalog"])
api_router.include_router(seller_products.router, prefix="/seller/products", tags=["seller-products"])
api_router.include_router(seller_dashboard.router, prefix="/seller/dashboard", tags=["seller-dashboard"])
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(admin_users.router, prefix="/admin/users", tags=["admin-users"])
api_router.include_router(admin_products.router, prefix="/admin/products", tags=["admin-products"])
api_router.include_router(admin_reviews.router, prefix="/admin/reviews", tags=["admin-reviews"])
api_router.include_router(admin_stats.router, prefix="/admin/stats", tags=["admin-stats"])
api_router.include_router(admin_audit.router, prefix="/admin/audit", tags=["admin-audit"])
