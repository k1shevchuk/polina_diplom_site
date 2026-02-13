import type { NavigationGuardNext, RouteLocationNormalized } from "vue-router";

import { useAuthStore } from "../stores/auth";

export async function authGuard(to: RouteLocationNormalized, _from: RouteLocationNormalized, next: NavigationGuardNext) {
  const auth = useAuthStore();

  if (!auth.token) {
    if (to.meta.public) {
      next();
      return;
    }
    next("/auth/login");
    return;
  }

  if (!auth.me) {
    try {
      await auth.fetchMe();
    } catch {
      next("/auth/login");
      return;
    }
  }

  if (auth.me?.is_banned) {
    await auth.logout();
    next("/auth/login");
    return;
  }

  const requiredRoles = (to.meta.roles as string[] | undefined) ?? [];
  if (requiredRoles.length > 0) {
    const hasAny = requiredRoles.some((role) => auth.hasRole(role as any));
    if (!hasAny) {
      next("/");
      return;
    }
  }

  next();
}
