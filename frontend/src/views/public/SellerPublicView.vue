<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import { formatCurrency } from "../../shared/utils/currency";
import { cleanText } from "../../shared/utils/text";

interface SellerPublicProduct {
  id: number;
  title: string;
  description: string;
  price: string;
  stock: number | null;
  image_url: string | null;
}

interface SellerPublicResponse {
  seller_id: number;
  display_name: string;
  bio: string | null;
  products: SellerPublicProduct[];
}

const route = useRoute();
const isLoading = ref(true);
const seller = ref<SellerPublicResponse | null>(null);
const isNotFound = ref(false);

const sellerId = computed(() => Number(route.params.id));

async function loadSeller() {
  isLoading.value = true;
  isNotFound.value = false;
  try {
    const response = await api.get<SellerPublicResponse>(endpoints.seller.publicById(sellerId.value));
    seller.value = response.data;
  } catch {
    seller.value = null;
    isNotFound.value = true;
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadSeller);

watch(
  () => route.params.id,
  () => {
    loadSeller();
  },
);
</script>

<template>
  <section class="space-y-6">
    <UiSkeleton v-if="isLoading" :rows="4" />

    <section v-else-if="seller" class="space-y-5">
      <header class="rounded-2xl bg-white p-6 shadow-soft">
        <h1 class="font-display text-4xl font-bold text-primary-dark">{{ seller.display_name }}</h1>
        <p class="mt-2 text-[1.05rem] text-muted">{{ seller.bio || "Продавец Craft With Love" }}</p>
      </header>

      <section>
        <h2 class="mb-4 font-display text-3xl font-bold text-primary-dark">Товары продавца</h2>

        <div v-if="seller.products.length === 0" class="brand-empty-state p-6 text-center text-[1.05rem] text-muted">
          У этого продавца пока нет активных товаров.
        </div>

        <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <article v-for="product in seller.products" :key="product.id" class="brand-product-card">
            <img
              :src="product.image_url || '/brand/products/scarf1.jpg'"
              :alt="cleanText(product.title, 'Вязаное изделие')"
              class="h-56 w-full object-cover"
              loading="lazy"
            />
            <div class="space-y-2 p-4">
              <router-link :to="`/product/${product.id}`" class="block text-2xl font-semibold text-primary-dark">
                {{ cleanText(product.title, "Вязаное изделие") }}
              </router-link>
              <p class="line-clamp-2 text-sm text-muted">{{ cleanText(product.description, "Описание временно недоступно") }}</p>
              <div class="flex items-center justify-between">
                <strong class="text-2xl text-primary-dark">{{ formatCurrency(product.price) }}</strong>
                <router-link :to="`/product/${product.id}`" class="text-sm font-semibold text-primary-dark">Подробнее</router-link>
              </div>
            </div>
          </article>
        </div>
      </section>
    </section>

    <section v-else class="brand-empty-state p-8 text-center">
      <h2 class="font-display text-3xl font-bold text-primary-dark">Профиль продавца не найден</h2>
      <p class="mt-2 text-[1.05rem] text-muted">Проверьте ссылку или вернитесь в каталог.</p>
      <router-link to="/catalog" class="brand-btn mt-4 px-5 py-2">В каталог</router-link>
    </section>
  </section>
</template>
