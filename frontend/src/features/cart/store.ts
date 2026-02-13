import { defineStore } from "pinia";
import { ref } from "vue";

import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { Cart } from "../../shared/types/order";

export const useCartStore = defineStore("cart", () => {
  const cart = ref<Cart | null>(null);
  const isLoading = ref(false);

  async function fetchCart() {
    isLoading.value = true;
    try {
      const response = await api.get<Cart>(endpoints.cart);
      cart.value = response.data;
    } finally {
      isLoading.value = false;
    }
  }

  async function addItem(productId: number, qty = 1) {
    const response = await api.post<Cart>(`${endpoints.cart}/items`, { product_id: productId, qty });
    cart.value = response.data;
  }

  async function removeItem(itemId: number) {
    const response = await api.delete<Cart>(`${endpoints.cart}/items/${itemId}`);
    cart.value = response.data;
  }

  return { cart, isLoading, fetchCart, addItem, removeItem };
});

