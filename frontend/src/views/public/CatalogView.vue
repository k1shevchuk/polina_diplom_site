<script setup lang="ts">
import { computed, ref, watch } from "vue";

import UiButton from "../../components/ui/UiButton.vue";
import UiCard from "../../components/ui/UiCard.vue";
import UiDropdown from "../../components/ui/UiDropdown.vue";
import UiInput from "../../components/ui/UiInput.vue";
import UiPagination from "../../components/ui/UiPagination.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useDebounce } from "../../composables/useDebounce";
import { useCatalogStore } from "../../features/catalog/store";
import { formatCurrency } from "../../shared/utils/currency";

const store = useCatalogStore();

const q = ref("");
const minPrice = ref("");
const maxPrice = ref("");
const sort = ref("new");
const page = ref(1);
const filtersOpen = ref(false);

const debounced = useDebounce<string>(400);
watch(q, (value) => debounced.set(value));
watch(
  () => debounced.value.value,
  () => {
    page.value = 1;
    load();
  },
);

watch([sort], () => {
  page.value = 1;
  load();
});

function load() {
  store.fetchCatalog({
    q: debounced.value.value || undefined,
    min_price: minPrice.value || undefined,
    max_price: maxPrice.value || undefined,
    sort: sort.value,
    page: page.value,
  });
}

function applyFilters() {
  page.value = 1;
  filtersOpen.value = false;
  load();
}

load();

const empty = computed(() => !store.isLoading && store.products.length === 0);
</script>

<template>
  <section class="space-y-4">
    <header class="flex flex-col gap-3 rounded-2xl bg-white p-4 shadow-soft md:flex-row md:items-center md:justify-between">
      <UiInput v-model="q" label="Поиск" placeholder="Например, керамическая ваза" aria-label="Поиск товаров" />
      <div class="hidden gap-2 md:flex">
        <UiInput v-model="minPrice" label="Мин. цена" type="number" />
        <UiInput v-model="maxPrice" label="Макс. цена" type="number" />
        <UiDropdown
          v-model="sort"
          aria-label="Сортировка"
          :options="[
            { value: 'new', label: 'Сначала новые' },
            { value: 'price_asc', label: 'Сначала дешевле' },
            { value: 'price_desc', label: 'Сначала дороже' },
          ]"
        />
        <UiButton @click="applyFilters">Применить</UiButton>
      </div>
      <UiButton class="md:hidden" variant="secondary" @click="filtersOpen = true">Фильтры</UiButton>
    </header>

    <transition name="fade">
      <div v-if="filtersOpen" class="fixed inset-0 z-50 bg-black/40 md:hidden" @click.self="filtersOpen = false">
        <div class="absolute bottom-0 w-full rounded-t-3xl bg-white p-4">
          <h3 class="mb-3 font-display text-lg font-bold">Фильтры</h3>
          <div class="space-y-3">
            <UiInput v-model="minPrice" label="Мин. цена" type="number" />
            <UiInput v-model="maxPrice" label="Макс. цена" type="number" />
            <UiDropdown
              v-model="sort"
              aria-label="Сортировка"
              :options="[
                { value: 'new', label: 'Сначала новые' },
                { value: 'price_asc', label: 'Сначала дешевле' },
                { value: 'price_desc', label: 'Сначала дороже' },
              ]"
            />
            <UiButton class="w-full" @click="applyFilters">Показать товары</UiButton>
          </div>
        </div>
      </div>
    </transition>

    <UiSkeleton v-if="store.isLoading" :rows="6" />

    <div v-else-if="empty" class="rounded-2xl border border-dashed border-brand-300 bg-white p-8 text-center">
      <h3 class="font-display text-xl font-bold">Товары не найдены</h3>
      <p class="mt-2 text-sm text-ink/70">Попробуйте изменить фильтры или убрать часть условий.</p>
      <UiButton class="mt-4" @click="q = ''; minPrice = ''; maxPrice = ''; sort = 'new'; load()">Сбросить фильтры</UiButton>
    </div>

    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <UiCard v-for="item in store.products" :key="item.id">
        <img
          :src="item.images?.[0]?.image_url || 'https://placehold.co/600x400?text=Handmade'"
          :alt="item.title"
          class="mb-3 h-40 w-full rounded-xl object-cover"
        />
        <h3 class="font-display text-lg font-bold">{{ item.title }}</h3>
        <p class="mt-1 line-clamp-2 text-sm text-ink/70">{{ item.description }}</p>
        <div class="mt-3 flex items-center justify-between">
          <strong class="text-brand-800">{{ formatCurrency(item.price) }}</strong>
          <router-link :to="`/product/${item.id}`" class="text-sm font-semibold">Подробнее</router-link>
        </div>
      </UiCard>
    </div>

    <UiPagination :page="page" :page-size="20" :total="store.total" @change="(value) => { page = value; load(); }" />
  </section>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

