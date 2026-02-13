import { defineStore } from "pinia";
import { ref } from "vue";

import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { Order } from "../../shared/types/order";

export const useOrdersStore = defineStore("orders", () => {
  const buyerOrders = ref<Order[]>([]);
  const sellerOrders = ref<Order[]>([]);
  const isLoading = ref(false);

  async function fetchBuyerOrders() {
    isLoading.value = true;
    try {
      const response = await api.get<Order[]>(endpoints.orders.buyer);
      buyerOrders.value = response.data;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchSellerOrders() {
    isLoading.value = true;
    try {
      const response = await api.get<Order[]>(endpoints.orders.seller);
      sellerOrders.value = response.data;
    } finally {
      isLoading.value = false;
    }
  }

  return { buyerOrders, sellerOrders, isLoading, fetchBuyerOrders, fetchSellerOrders };
});
