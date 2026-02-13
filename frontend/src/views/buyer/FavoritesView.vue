<script setup lang="ts">
import { onMounted } from "vue";

import UiCard from "../../components/ui/UiCard.vue";
import { useFavoritesStore } from "../../features/favorites/store";

const store = useFavoritesStore();

onMounted(() => {
  store.fetchFavorites();
});
</script>

<template>
  <section>
    <h1 class="mb-4 font-display text-2xl font-bold">Избранное</h1>
    <div v-if="store.items.length === 0" class="rounded-2xl border border-dashed border-brand-300 p-6 text-center">
      <h2 class="font-display text-xl font-bold">Нет избранных товаров</h2>
      <router-link to="/catalog" class="mt-2 inline-block text-sm font-semibold">Перейти в каталог</router-link>
    </div>
    <div v-else class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      <UiCard v-for="id in store.items" :key="id">
        <p class="font-semibold">Товар #{{ id }}</p>
        <router-link :to="`/product/${id}`" class="text-sm">Открыть</router-link>
      </UiCard>
    </div>
  </section>
</template>

