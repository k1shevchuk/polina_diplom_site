import { defineStore } from "pinia";
import { ref } from "vue";

import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";

export const useFavoritesStore = defineStore("favorites", () => {
  const items = ref<number[]>([]);

  async function fetchFavorites() {
    const response = await api.get<number[]>(endpoints.favorites);
    items.value = response.data;
  }

  async function toggleFavorite(productId: number) {
    if (items.value.includes(productId)) {
      await api.delete(`${endpoints.favorites}/${productId}`);
      items.value = items.value.filter((id) => id !== productId);
    } else {
      await api.post(`${endpoints.favorites}/${productId}`);
      items.value.push(productId);
    }
  }

  return { items, fetchFavorites, toggleFavorite };
});

