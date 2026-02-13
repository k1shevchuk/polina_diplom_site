<script setup lang="ts">
import { onMounted, ref } from "vue";

import UiCard from "../../components/ui/UiCard.vue";
import { api } from "../../shared/api/client";

const stats = ref<any>(null);
const trend = ref<any[]>([]);

onMounted(async () => {
  const statsResponse = await api.get("/admin/stats");
  const trendResponse = await api.get("/admin/stats/trend");
  stats.value = statsResponse.data;
  trend.value = trendResponse.data;
});
</script>

<template>
  <section class="space-y-4">
    <h1 class="font-display text-2xl font-bold">Статистика</h1>
    <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
      <UiCard><p class="text-xs text-ink/70">Пользователи</p><p class="text-xl font-bold">{{ stats?.users || 0 }}</p></UiCard>
      <UiCard><p class="text-xs text-ink/70">Продавцы</p><p class="text-xl font-bold">{{ stats?.sellers || 0 }}</p></UiCard>
      <UiCard><p class="text-xs text-ink/70">Товары</p><p class="text-xl font-bold">{{ stats?.products || 0 }}</p></UiCard>
      <UiCard><p class="text-xs text-ink/70">Заказы</p><p class="text-xl font-bold">{{ stats?.orders || 0 }}</p></UiCard>
      <UiCard><p class="text-xs text-ink/70">Отзывы</p><p class="text-xl font-bold">{{ stats?.reviews || 0 }}</p></UiCard>
    </div>

    <UiCard>
      <h2 class="mb-2 font-display text-lg font-bold">Тренд заказов по дням</h2>
      <div class="space-y-2">
        <div v-for="row in trend" :key="row.day" class="flex items-center gap-3 text-sm">
          <span class="w-28">{{ row.day }}</span>
          <div class="h-3 rounded bg-brand-500" :style="{ width: `${row.count * 20}px` }" />
          <span>{{ row.count }}</span>
        </div>
      </div>
    </UiCard>
  </section>
</template>

