<script setup lang="ts">
import { onMounted, ref } from "vue";

import UiCard from "../../components/ui/UiCard.vue";
import { api } from "../../shared/api/client";

const data = ref<{ products: number; orders: number } | null>(null);

onMounted(async () => {
  const response = await api.get("/seller/dashboard");
  data.value = response.data;
});
</script>

<template>
  <section>
    <h1 class="mb-4 font-display text-2xl font-bold">Дашборд продавца</h1>
    <div class="grid gap-3 md:grid-cols-2">
      <UiCard>
        <p class="text-sm text-ink/70">Товары</p>
        <p class="font-display text-3xl font-extrabold">{{ data?.products ?? 0 }}</p>
      </UiCard>
      <UiCard>
        <p class="text-sm text-ink/70">Заказы</p>
        <p class="font-display text-3xl font-extrabold">{{ data?.orders ?? 0 }}</p>
      </UiCard>
    </div>
  </section>
</template>

