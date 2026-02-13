import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { NotificationItem } from "../../shared/types/notification";

export const useNotificationsStore = defineStore("notifications", () => {
  const items = ref<NotificationItem[]>([]);

  const unreadCount = computed(() => items.value.filter((item) => !item.is_read).length);

  async function fetchNotifications() {
    const response = await api.get<NotificationItem[]>(endpoints.notifications);
    items.value = response.data;
  }

  async function markAsRead(id: number) {
    const existing = items.value.find((item) => item.id === id);
    if (!existing) return;
    existing.is_read = true;
    try {
      await api.post(`${endpoints.notifications}/${id}/read`);
    } catch (error) {
      existing.is_read = false;
      throw error;
    }
  }

  return { items, unreadCount, fetchNotifications, markAsRead };
});

