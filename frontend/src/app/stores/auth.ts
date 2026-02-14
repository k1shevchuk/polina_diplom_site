import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { api, setAccessToken } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { RoleName, UserMe } from "../../shared/types/auth";

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(null);
  const me = ref<UserMe | null>(null);
  const isLoading = ref(false);

  const isAuthenticated = computed(() => Boolean(token.value && me.value));
  const roles = computed<RoleName[]>(() => me.value?.roles ?? []);

  function hasRole(role: RoleName): boolean {
    return roles.value.includes(role);
  }

  async function register(email: string, password: string) {
    isLoading.value = true;
    try {
      const response = await api.post(endpoints.auth.register, { email, password });
      token.value = response.data.access_token;
      setAccessToken(token.value);
      await fetchMe();
    } finally {
      isLoading.value = false;
    }
  }

  async function login(email: string, password: string) {
    isLoading.value = true;
    try {
      const response = await api.post(endpoints.auth.login, { email, password });
      token.value = response.data.access_token;
      setAccessToken(token.value);
      await fetchMe();
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchMe() {
    const response = await api.get<UserMe>(endpoints.auth.me);
    me.value = response.data;
  }

  async function refresh() {
    const response = await api.post(endpoints.auth.refresh);
    token.value = response.data.access_token;
    setAccessToken(token.value);
    await fetchMe();
  }

  async function logout() {
    try {
      await api.post(endpoints.auth.logout);
    } catch {
      // Local logout must still complete even if backend session is already expired.
    } finally {
      token.value = null;
      me.value = null;
      setAccessToken(null);
    }
  }

  async function toggleSeller(enabled = true) {
    const response = await api.post(`${endpoints.auth.sellerRole}?enabled=${enabled}`);
    me.value = response.data;
  }

  return {
    token,
    me,
    isLoading,
    isAuthenticated,
    roles,
    hasRole,
    register,
    login,
    fetchMe,
    refresh,
    logout,
    toggleSeller,
  };
});

