<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { AxiosError } from "axios";

import UiButton from "../../components/ui/UiButton.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { Product } from "../../shared/types/product";

interface SellerProfileResponse {
  seller_id: number;
  display_name: string;
  bio: string | null;
}

const ui = useUiStore();
const isLoading = ref(true);
const isSaving = ref(false);
const products = ref<Product[]>([]);
const isProductsLoading = ref(true);

const form = reactive({
  display_name: "",
  bio: "",
});

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
  return "Не удалось сохранить профиль";
}

async function loadProfile() {
  isLoading.value = true;
  try {
    const response = await api.get<SellerProfileResponse>(endpoints.seller.profile);
    form.display_name = response.data.display_name;
    form.bio = response.data.bio || "";
  } catch {
    ui.pushToast("error", "Не удалось загрузить профиль продавца");
  } finally {
    isLoading.value = false;
  }
}

async function loadProducts() {
  isProductsLoading.value = true;
  try {
    const response = await api.get<{ items: Product[] }>(endpoints.seller.products);
    products.value = response.data.items;
  } catch {
    products.value = [];
    ui.pushToast("error", "Не удалось загрузить товары продавца");
  } finally {
    isProductsLoading.value = false;
  }
}

async function saveProfile() {
  isSaving.value = true;
  try {
    await api.put<SellerProfileResponse>(endpoints.seller.profile, {
      display_name: form.display_name.trim(),
      bio: form.bio.trim() || null,
    });
    ui.pushToast("success", "Профиль продавца обновлён");
  } catch (error) {
    ui.pushToast("error", extractApiError(error));
  } finally {
    isSaving.value = false;
  }
}

onMounted(async () => {
  await Promise.all([loadProfile(), loadProducts()]);
});
</script>

<template>
  <section class="space-y-4">
    <UiSkeleton v-if="isLoading" :rows="4" />

    <template v-else>
      <h1 class="font-display text-2xl font-bold text-primary-dark">Профиль продавца</h1>

      <form class="space-y-3" @submit.prevent="saveProfile">
        <label class="flex flex-col gap-1 text-[1.03rem] font-semibold text-primary-dark">
          <span>Название витрины</span>
          <input v-model="form.display_name" class="brand-input px-3 py-2.5 text-[1.03rem] outline-none" />
        </label>

        <label class="flex flex-col gap-1 text-[1.03rem] font-semibold text-primary-dark">
          <span>Описание продавца</span>
          <textarea
            v-model="form.bio"
            rows="5"
            class="brand-textarea px-3 py-2.5 text-[1.03rem] outline-none"
            placeholder="Расскажите о мастерской, материалах и сроках изготовления"
          />
        </label>

        <UiButton type="submit" :disabled="isSaving">Сохранить профиль</UiButton>
      </form>

      <section class="space-y-3 rounded-2xl border border-brand-200 bg-white p-4">
        <div class="flex items-center justify-between gap-3">
          <h2 class="font-display text-xl font-bold text-primary-dark">Мои товары</h2>
          <router-link to="/seller/products" class="text-sm font-semibold text-primary-dark">Открыть все</router-link>
        </div>

        <UiSkeleton v-if="isProductsLoading" :rows="3" />

        <div v-else-if="products.length === 0" class="brand-empty-state p-4 text-center">
          Товары пока не добавлены.
          <router-link to="/seller/products/new" class="ml-1 font-semibold text-primary-dark">Создать первый товар</router-link>
        </div>

        <div v-else class="space-y-2">
          <article
            v-for="item in products.slice(0, 5)"
            :key="item.id"
            class="flex items-center justify-between gap-3 rounded-xl border border-brand-100 bg-brand-50/60 p-3"
          >
            <div class="min-w-0">
              <p class="line-clamp-1 text-sm font-semibold text-primary-dark">{{ item.title }}</p>
              <p class="text-xs text-muted">Статус: {{ item.status }} · Цена: {{ item.price }} ₽</p>
            </div>
            <router-link :to="`/seller/products/${item.id}/edit`" class="text-sm font-semibold text-primary-dark">Редактировать</router-link>
          </article>
        </div>
      </section>
    </template>
  </section>
</template>
