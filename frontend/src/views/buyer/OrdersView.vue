<script setup lang="ts">
import { onMounted } from "vue";

import UiBadge from "../../components/ui/UiBadge.vue";
import UiCard from "../../components/ui/UiCard.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useOrdersStore } from "../../features/orders/store";
import { formatCurrency } from "../../shared/utils/currency";
import { formatDate } from "../../shared/utils/date";

const store = useOrdersStore();

onMounted(() => {
  store.fetchBuyerOrders();
});
</script>

<template>
  <section>
    <h1 class="mb-4 font-display text-2xl font-bold">Мои заказы</h1>
    <UiSkeleton v-if="store.isLoading" :rows="4" />

    <div v-else-if="store.buyerOrders.length === 0" class="rounded-2xl border border-dashed border-brand-300 p-6 text-center">
      <h2 class="font-display text-xl font-bold">Пока нет заказов</h2>
      <router-link to="/catalog" class="mt-2 inline-block text-sm font-semibold">Выбрать товары</router-link>
    </div>

    <div v-else class="space-y-3">
      <UiCard v-for="order in store.buyerOrders" :key="order.id" class="space-y-2">
        <div class="flex items-center justify-between">
          <h3 class="font-semibold">Заказ #{{ order.id }}</h3>
          <UiBadge>{{ order.status }}</UiBadge>
        </div>
        <p class="text-sm text-ink/70">{{ formatDate(order.created_at) }}</p>
        <p class="text-sm">Сумма: <strong>{{ formatCurrency(order.total_amount) }}</strong></p>
        <router-link :to="`/orders/${order.id}`" class="text-sm">Подробнее</router-link>
      </UiCard>
    </div>
  </section>
</template>

