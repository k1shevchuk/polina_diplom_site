<script setup lang="ts">
import { onMounted, ref } from "vue";

import UiButton from "../../components/ui/UiButton.vue";
import UiCard from "../../components/ui/UiCard.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";

const ui = useUiStore();
const products = ref<any[]>([]);

async function load() {
  const response = await api.get("/admin/products");
  products.value = response.data.items;
}

async function moderate(id: number, approve: boolean) {
  await api.post(`/admin/products/${id}/moderate`, { approve, reason: approve ? null : "Не соответствует правилам" });
  ui.pushToast("success", approve ? "Товар одобрен" : "Товар отклонён");
  load();
}

onMounted(load);
</script>

<template>
  <section>
    <h1 class="mb-4 font-display text-2xl font-bold">Модерация товаров</h1>
    <div v-if="products.length === 0" class="rounded-2xl border border-dashed border-brand-300 p-6 text-center">Очередь пуста</div>
    <div v-else class="space-y-3">
      <UiCard v-for="item in products" :key="item.id" class="flex items-center justify-between gap-3">
        <div>
          <h3 class="font-semibold">{{ item.title }}</h3>
          <p class="text-sm text-ink/70">Продавец #{{ item.seller_id }}</p>
        </div>
        <div class="flex gap-2">
          <UiButton variant="secondary" @click="moderate(item.id, true)">Одобрить</UiButton>
          <UiButton variant="danger" @click="moderate(item.id, false)">Отклонить</UiButton>
        </div>
      </UiCard>
    </div>
  </section>
</template>

