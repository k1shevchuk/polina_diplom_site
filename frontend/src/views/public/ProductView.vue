<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute } from "vue-router";

import UiBadge from "../../components/ui/UiBadge.vue";
import UiButton from "../../components/ui/UiButton.vue";
import UiCard from "../../components/ui/UiCard.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useCartStore } from "../../features/cart/store";
import { useCatalogStore } from "../../features/catalog/store";
import { useFavoritesStore } from "../../features/favorites/store";
import { formatCurrency } from "../../shared/utils/currency";

const route = useRoute();
const catalogStore = useCatalogStore();
const cartStore = useCartStore();
const favoritesStore = useFavoritesStore();

const productId = Number(route.params.id);
const isLoading = ref(true);

catalogStore.fetchCatalog({ page_size: 100 }).finally(() => {
  isLoading.value = false;
});

const product = computed(() => catalogStore.products.find((item) => item.id === productId) || null);
const related = computed(() =>
  catalogStore.products.filter((item) => item.category_id === product.value?.category_id && item.id !== productId).slice(0, 4),
);

function addToCart() {
  if (!product.value) return;
  cartStore.addItem(product.value.id, 1);
}

function toggleFavorite() {
  if (!product.value) return;
  favoritesStore.toggleFavorite(product.value.id);
}
</script>

<template>
  <section class="space-y-6">
    <UiSkeleton v-if="isLoading" :rows="4" />

    <template v-else-if="product">
      <div class="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
        <div class="space-y-3">
          <img
            :src="product.images?.[0]?.image_url || 'https://placehold.co/800x600?text=Handmade+Product'"
            :alt="product.title"
            class="h-96 w-full rounded-2xl object-cover"
          />
          <div class="grid grid-cols-4 gap-2">
            <img
              v-for="index in 4"
              :key="index"
              :src="product.images?.[index - 1]?.image_url || 'https://placehold.co/200x150?text=Photo'"
              class="h-20 w-full rounded-xl object-cover"
              :alt="`Фото ${index}`"
            />
          </div>
        </div>

        <UiCard>
          <UiBadge>В наличии</UiBadge>
          <h1 class="mt-3 font-display text-3xl font-extrabold">{{ product.title }}</h1>
          <p class="mt-2 text-sm text-ink/75">{{ product.description }}</p>
          <p class="mt-4 text-3xl font-extrabold text-brand-800">{{ formatCurrency(product.price) }}</p>

          <div class="mt-5 flex gap-2">
            <UiButton @click="addToCart">Добавить в корзину</UiButton>
            <UiButton variant="secondary" @click="toggleFavorite">В избранное</UiButton>
          </div>

          <div class="mt-6 rounded-xl bg-brand-50 p-4">
            <p class="text-sm font-semibold">Продавец #{{ product.seller_id }}</p>
            <router-link :to="`/seller/${product.seller_id}`" class="text-sm">Открыть профиль продавца</router-link>
          </div>
        </UiCard>
      </div>

      <div class="rounded-2xl bg-white p-4 shadow-soft">
        <h2 class="font-display text-xl font-bold">Похожие товары</h2>
        <div class="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <UiCard v-for="item in related" :key="item.id">
            <h3 class="font-semibold">{{ item.title }}</h3>
            <p class="text-sm text-ink/70">{{ formatCurrency(item.price) }}</p>
            <router-link :to="`/product/${item.id}`" class="text-xs">Открыть</router-link>
          </UiCard>
        </div>
      </div>

      <div class="sticky bottom-2 z-30 rounded-2xl bg-white p-3 shadow-soft md:hidden">
        <div class="flex items-center justify-between gap-3">
          <strong>{{ formatCurrency(product.price) }}</strong>
          <div class="flex gap-2">
            <UiButton variant="secondary" @click="toggleFavorite">Избранное</UiButton>
            <UiButton @click="addToCart">Купить</UiButton>
          </div>
        </div>
      </div>
    </template>

    <div v-else class="rounded-2xl border border-dashed border-brand-300 bg-white p-8 text-center">
      <h3 class="font-display text-xl font-bold">Товар не найден</h3>
      <router-link class="mt-2 inline-block text-sm" to="/catalog">Вернуться в каталог</router-link>
    </div>
  </section>
</template>
