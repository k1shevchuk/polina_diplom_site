<script setup lang="ts">
import { onMounted, ref } from "vue";

import UiButton from "../../components/ui/UiButton.vue";
import UiCard from "../../components/ui/UiCard.vue";
import UiBadge from "../../components/ui/UiBadge.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";
import type { Product } from "../../shared/types/product";

const ui = useUiStore();
const products = ref<Product[]>([]);
const isLoading = ref(false);

async function load() {
  isLoading.value = true;
  try {
    const response = await api.get("/seller/products");
    products.value = response.data.items;
  } finally {
    isLoading.value = false;
  }
}

async function submitForModeration(id: number) {
  await api.post(`/seller/products/${id}/submit`);
  ui.pushToast("success", "Отправлено на модерацию");
  load();
}

function removeProduct(id: number) {
  ui.askConfirm({
    title: "Архивировать товар",
    message: "Товар будет скрыт из каталога",
    onConfirm: async () => {
      await api.delete(`/seller/products/${id}`);
      ui.pushToast("success", "Товар архивирован");
      load();
    },
  });
}

onMounted(load);
</script>

<template>
  <section>
    <div class="mb-4 flex items-center justify-between">
      <h1 class="font-display text-2xl font-bold">Мои товары</h1>
      <router-link to="/seller/products/new" class="rounded-xl bg-brand-600 px-4 py-2 text-sm font-bold text-white">Новый товар</router-link>
    </div>

    <div v-if="isLoading" class="space-y-2">
      <div class="h-20 animate-pulse rounded-xl bg-brand-100" />
      <div class="h-20 animate-pulse rounded-xl bg-brand-100" />
    </div>

    <div v-else-if="products.length === 0" class="rounded-2xl border border-dashed border-brand-300 p-6 text-center">
      Нет товаров. <router-link to="/seller/products/new">Добавить первый</router-link>
    </div>

    <div v-else class="space-y-3">
      <UiCard v-for="item in products" :key="item.id" class="flex items-center justify-between gap-3">
        <div>
          <h3 class="font-semibold">{{ item.title }}</h3>
          <UiBadge>{{ item.status }}</UiBadge>
        </div>
        <div class="flex flex-wrap gap-2">
          <router-link :to="`/seller/products/${item.id}/edit`" class="rounded-lg bg-brand-100 px-3 py-1 text-sm">Редактировать</router-link>
          <UiButton v-if="item.status === 'DRAFT' || item.status === 'REJECTED'" variant="secondary" @click="submitForModeration(item.id)">
            На модерацию
          </UiButton>
          <UiButton variant="danger" @click="removeProduct(item.id)">Архив</UiButton>
        </div>
      </UiCard>
    </div>
  </section>
</template>
