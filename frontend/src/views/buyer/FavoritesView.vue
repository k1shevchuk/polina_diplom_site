<script setup lang="ts">
import { computed, onMounted } from "vue";

import KnitProductCard from "../../components/catalog/KnitProductCard.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useCatalogStore } from "../../features/catalog/store";
import { useFavoritesStore } from "../../features/favorites/store";

const catalogStore = useCatalogStore();
const favoritesStore = useFavoritesStore();

const favoriteProducts = computed(() => catalogStore.products.filter((product) => favoritesStore.items.includes(product.id)));
const isLoading = computed(() => catalogStore.isLoading);

onMounted(async () => {
  await Promise.all([
    favoritesStore.fetchFavorites(),
    catalogStore.fetchCatalog({ page: 1, page_size: 100, sort: "new" }),
  ]);
});
</script>

<template>
  <section class="space-y-6">
    <header class="rounded-[20px] bg-[linear-gradient(135deg,rgba(255,209,228,0.85),rgba(255,210,227,0.95))] p-6 md:p-8">
      <h1 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Избранное</h1>
      <p class="mt-2 text-[1.16rem] text-primary-dark/85">Собрали товары, которые вам особенно понравились</p>
    </header>

    <UiSkeleton v-if="isLoading" :rows="4" />

    <section v-else-if="favoriteProducts.length === 0" class="brand-empty-state p-8 text-center">
      <h2 class="brand-title text-4xl font-bold text-primary-dark">Пока ничего нет</h2>
      <p class="mt-2 text-[1.12rem] text-muted">Добавляйте вязаные изделия в избранное, чтобы вернуться к ним позже.</p>
      <router-link to="/catalog" class="brand-btn mt-4 px-6 py-3">Открыть каталог</router-link>
    </section>

    <section v-else class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <KnitProductCard v-for="item in favoriteProducts" :key="item.id" :product="item" />
    </section>
  </section>
</template>
