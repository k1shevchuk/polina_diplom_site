<script setup lang="ts">
import { onMounted, ref } from "vue";
import { AxiosError } from "axios";

import UiButton from "../../components/ui/UiButton.vue";
import UiCard from "../../components/ui/UiCard.vue";
import UiBadge from "../../components/ui/UiBadge.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { Product } from "../../shared/types/product";

const ui = useUiStore();
const products = ref<Product[]>([]);
const isLoading = ref(false);

function extractApiError(error: unknown): string {
  if (error instanceof AxiosError && typeof error.response?.data?.detail === "string") {
    return error.response.data.detail;
  }
  return "Не удалось загрузить товары продавца";
}

async function load() {
  isLoading.value = true;
  try {
    const response = await api.get<{ items: Product[] }>(endpoints.seller.products);
    products.value = response.data.items;
  } catch (error) {
    products.value = [];
    ui.pushToast("error", extractApiError(error));
  } finally {
    isLoading.value = false;
  }
}

async function submitForModeration(id: number) {
  try {
    await api.post(`${endpoints.seller.products}/${id}/submit`);
    ui.pushToast("success", "Товар отправлен на модерацию");
    await load();
  } catch (error) {
    ui.pushToast("error", extractApiError(error));
  }
}

function archiveProduct(id: number) {
  ui.askConfirm({
    title: "Архивировать товар",
    message: "Товар будет скрыт из каталога.",
    onConfirm: async () => {
      try {
        await api.delete(`${endpoints.seller.products}/${id}`);
        ui.pushToast("success", "Товар архивирован");
        await load();
      } catch (error) {
        ui.pushToast("error", extractApiError(error));
      }
    },
  });
}

onMounted(load);
</script>

<template>
  <section class="space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <h1 class="font-display text-2xl font-bold text-primary-dark">Мои товары</h1>
      <router-link to="/seller/products/new" class="brand-btn px-4 py-2 text-sm">Новый товар</router-link>
    </div>

    <UiSkeleton v-if="isLoading" :rows="3" />

    <div v-else-if="products.length === 0" class="brand-empty-state p-6 text-center">
      Товары пока не добавлены.
      <router-link to="/seller/products/new" class="ml-1 font-semibold text-primary-dark">Создать первый товар</router-link>
    </div>

    <div v-else class="space-y-3">
      <UiCard v-for="item in products" :key="item.id" class="flex flex-wrap items-center justify-between gap-3">
        <div class="space-y-1">
          <h3 class="font-semibold text-primary-dark">{{ item.title }}</h3>
          <UiBadge>{{ item.status }}</UiBadge>
          <p v-if="item.rejection_reason" class="text-xs text-red-700">Причина отклонения: {{ item.rejection_reason }}</p>
        </div>

        <div class="flex flex-wrap gap-2">
          <router-link :to="`/seller/products/${item.id}/edit`" class="rounded-lg bg-brand-100 px-3 py-1 text-sm">
            Редактировать
          </router-link>
          <UiButton
            v-if="item.status === 'DRAFT' || item.status === 'REJECTED'"
            variant="secondary"
            @click="submitForModeration(item.id)"
          >
            На модерацию
          </UiButton>
          <UiButton variant="danger" @click="archiveProduct(item.id)">Архив</UiButton>
        </div>
      </UiCard>
    </div>
  </section>
</template>
