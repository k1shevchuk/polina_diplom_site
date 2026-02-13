<script setup lang="ts">
import { onMounted } from "vue";

import UiButton from "../../components/ui/UiButton.vue";
import UiCard from "../../components/ui/UiCard.vue";
import { usePolling } from "../../composables/usePolling";
import { useNotificationsStore } from "../../features/notifications/store";
import { formatDate } from "../../shared/utils/date";

const store = useNotificationsStore();

onMounted(() => {
  store.fetchNotifications();
});

usePolling(async () => {
  await store.fetchNotifications();
}, 15000);
</script>

<template>
  <section>
    <div class="mb-4 flex items-center justify-between">
      <h1 class="font-display text-2xl font-bold">Уведомления</h1>
      <p class="text-sm">Непрочитано: {{ store.unreadCount }}</p>
    </div>

    <div v-if="store.items.length === 0" class="rounded-2xl border border-dashed border-brand-300 p-6 text-center">
      Нет уведомлений
    </div>

    <div v-else class="space-y-3">
      <UiCard v-for="item in store.items" :key="item.id" class="flex items-center justify-between gap-3">
        <div>
          <p class="font-semibold">{{ item.type }}</p>
          <p class="text-xs text-ink/70">{{ formatDate(item.created_at) }}</p>
        </div>
        <UiButton v-if="!item.is_read" variant="secondary" @click="store.markAsRead(item.id)">Прочитано</UiButton>
      </UiCard>
    </div>
  </section>
</template>
