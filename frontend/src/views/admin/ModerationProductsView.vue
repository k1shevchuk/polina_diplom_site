<script setup lang="ts">
import { onMounted, ref } from "vue";
import { AxiosError } from "axios";

import UiButton from "../../components/ui/UiButton.vue";
import UiCard from "../../components/ui/UiCard.vue";
import UiInput from "../../components/ui/UiInput.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { Product } from "../../shared/types/product";

const ui = useUiStore();
const products = ref<Product[]>([]);
const rejectReason = ref("Не соответствует правилам площадки");
const isLoading = ref(false);

function extractApiError(error: unknown): string {
  if (error instanceof AxiosError) {
    const detail = error.response?.data?.detail;
    if (Array.isArray(detail) && detail.length > 0) {
      return detail.map((item: { msg?: string }) => item.msg || "Validation error").join("; ");
    }
    if (typeof detail === "string") {
      return detail;
    }
  }
  return "Не удалось выполнить модерацию";
}

async function load() {
  isLoading.value = true;
  try {
    const response = await api.get<{ items: Product[] }>(`${endpoints.admin.products}?pending_only=true`);
    products.value = response.data.items;
  } catch (error) {
    products.value = [];
    ui.pushToast("error", extractApiError(error));
  } finally {
    isLoading.value = false;
  }
}

async function moderate(id: number, approve: boolean) {
  try {
    await api.post(`${endpoints.admin.products}/${id}/moderate`, {
      approve,
      reason: approve ? null : rejectReason.value.trim() || "Отклонено модератором",
    });
    ui.pushToast("success", approve ? "Товар одобрен" : "Товар отклонён");
    await load();
  } catch (error) {
    ui.pushToast("error", extractApiError(error));
  }
}

onMounted(load);
</script>

<template>
  <section class="space-y-4">
    <h1 class="font-display text-2xl font-bold text-primary-dark">Очередь модерации</h1>

    <UiInput v-model="rejectReason" label="Причина отклонения по умолчанию" />

    <UiSkeleton v-if="isLoading" :rows="3" />

    <div v-else-if="products.length === 0" class="brand-empty-state p-6 text-center">Очередь модерации пуста</div>

    <div v-else class="space-y-3">
      <UiCard v-for="item in products" :key="item.id" class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 class="font-semibold text-primary-dark">{{ item.title }}</h3>
          <p class="text-sm text-muted">Продавец #{{ item.seller_id }}</p>
        </div>
        <div class="flex gap-2">
          <UiButton variant="secondary" @click="moderate(item.id, true)">Одобрить</UiButton>
          <UiButton variant="danger" @click="moderate(item.id, false)">Отклонить</UiButton>
        </div>
      </UiCard>
    </div>
  </section>
</template>
