<script setup lang="ts">
import { onMounted, ref } from "vue";
import { AxiosError } from "axios";

import UiButton from "../../components/ui/UiButton.vue";
import UiCard from "../../components/ui/UiCard.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";

interface AdminReview {
  id: number;
  user_id: number;
  product_id: number;
  order_item_id: number;
  rating: number;
  text: string;
  is_hidden: boolean;
  created_at: string;
}

const ui = useUiStore();
const reviews = ref<AdminReview[]>([]);
const isLoading = ref(false);

function extractApiError(error: unknown): string {
  if (error instanceof AxiosError && typeof error.response?.data?.detail === "string") {
    return error.response.data.detail;
  }
  return "Ошибка работы с отзывом";
}

async function load() {
  isLoading.value = true;
  try {
    const response = await api.get<AdminReview[]>(endpoints.admin.reviews);
    reviews.value = response.data;
  } catch (error) {
    reviews.value = [];
    ui.pushToast("error", extractApiError(error));
  } finally {
    isLoading.value = false;
  }
}

async function toggleHide(review: AdminReview) {
  try {
    await api.post(`${endpoints.admin.reviews}/${review.id}/hide?hidden=${!review.is_hidden}`);
    ui.pushToast("success", review.is_hidden ? "Отзыв снова показан" : "Отзыв скрыт");
    await load();
  } catch (error) {
    ui.pushToast("error", extractApiError(error));
  }
}

function deleteReview(review: AdminReview) {
  ui.askConfirm({
    title: "Удалить отзыв",
    message: "Отзыв будет удалён безвозвратно.",
    onConfirm: async () => {
      try {
        await api.delete(`${endpoints.admin.reviews}/${review.id}`);
        ui.pushToast("success", "Отзыв удалён");
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
    <h1 class="font-display text-2xl font-bold text-primary-dark">Отзывы</h1>

    <UiSkeleton v-if="isLoading" :rows="3" />

    <div v-else-if="reviews.length === 0" class="brand-empty-state p-6 text-center">Отзывов пока нет</div>

    <div v-else class="space-y-3">
      <UiCard v-for="review in reviews" :key="review.id" class="space-y-2">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <p class="text-sm font-semibold text-primary-dark">Отзыв #{{ review.id }} · Product #{{ review.product_id }} · Rating {{ review.rating }}/5</p>
          <span class="text-xs text-muted">{{ review.created_at }}</span>
        </div>
        <p class="text-sm text-muted">{{ review.text }}</p>
        <div class="flex gap-2">
          <UiButton variant="secondary" @click="toggleHide(review)">
            {{ review.is_hidden ? "Показать" : "Скрыть" }}
          </UiButton>
          <UiButton variant="danger" @click="deleteReview(review)">Удалить</UiButton>
        </div>
      </UiCard>
    </div>
  </section>
</template>
