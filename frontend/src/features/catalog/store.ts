import { defineStore } from "pinia";
import { ref } from "vue";

import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { Product, Paginated } from "../../shared/types/product";

export const useCatalogStore = defineStore("catalog", () => {
  const products = ref<Product[]>([]);
  const total = ref(0);
  const isLoading = ref(false);

  async function fetchCatalog(params: Record<string, string | number | undefined>) {
    isLoading.value = true;
    try {
      const response = await api.get<Paginated<Product>>(endpoints.catalog, { params });
      products.value = response.data.items;
      total.value = response.data.meta.total;
    } finally {
      isLoading.value = false;
    }
  }

  return { products, total, isLoading, fetchCatalog };
});

