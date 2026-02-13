import { defineStore } from "pinia";
import { ref } from "vue";

import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { CheckoutResponse } from "../../shared/types/order";

export const useCheckoutStore = defineStore("checkout", () => {
  const lastCheckout = ref<CheckoutResponse | null>(null);
  const isLoading = ref(false);

  async function checkout(payload: { full_name: string; phone: string; address: string; comment?: string }) {
    isLoading.value = true;
    try {
      const response = await api.post<CheckoutResponse>(endpoints.checkout, payload);
      lastCheckout.value = response.data;
      return response.data;
    } finally {
      isLoading.value = false;
    }
  }

  return { lastCheckout, isLoading, checkout };
});

