<script setup lang="ts">
import { onMounted } from "vue";

import UiBadge from "../../components/ui/UiBadge.vue";
import UiCard from "../../components/ui/UiCard.vue";
import { useOrdersStore } from "../../features/orders/store";
import { formatCurrency } from "../../shared/utils/currency";

const store = useOrdersStore();
onMounted(() => {
  store.fetchSellerOrders();
});
</script>

<template>
  <section>
    <h1 class="mb-4 font-display text-2xl font-bold">Заказы продавца</h1>
    <div v-if="store.sellerOrders.length === 0" class="rounded-2xl border border-dashed border-brand-300 p-6 text-center">
      Заказов пока нет
    </div>
    <div v-else class="space-y-3">
      <UiCard v-for="order in store.sellerOrders" :key="order.id" class="flex items-center justify-between">
        <div>
          <p class="font-semibold">Заказ #{{ order.id }}</p>
          <p class="text-sm">{{ formatCurrency(order.total_amount) }}</p>
        </div>
        <UiBadge>{{ order.status }}</UiBadge>
      </UiCard>
    </div>
  </section>
</template>
