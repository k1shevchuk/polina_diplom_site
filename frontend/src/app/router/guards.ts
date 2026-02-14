import type { RouteLocationNormalized } from "vue-router";

import { useAuthStore } from "../stores/auth";

export async function authGuard(to: RouteLocationNormalized) {
  const auth = useAuthStore();

  if (!auth.token && !to.meta.public) {
    try {
      await auth.refresh();
    } catch {
      return "/auth/login";
    }
  }

  if (auth.token && !auth.me) {
    try {
      await auth.fetchMe();
    } catch {
      return "/auth/login";
    }
  }

  if (auth.me?.is_banned) {
    await auth.logout();
    return "/auth/login";
  }

  const requiredRoles = (to.meta.roles as string[] | undefined) ?? [];
  if (requiredRoles.length > 0) {
    const hasAny = requiredRoles.some((role) => auth.hasRole(role as any));
    if (!hasAny) {
      return "/";
    }
  }

  return true;
}
