<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";

import KnitProductCard from "../../components/catalog/KnitProductCard.vue";
import UiButton from "../../components/ui/UiButton.vue";
import UiDropdown from "../../components/ui/UiDropdown.vue";
import UiInput from "../../components/ui/UiInput.vue";
import UiPagination from "../../components/ui/UiPagination.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useAuthStore } from "../../app/stores/auth";
import { useDebounce } from "../../composables/useDebounce";
import { useCatalogStore } from "../../features/catalog/store";
import { useFavoritesStore } from "../../features/favorites/store";

const auth = useAuthStore();
const catalog = useCatalogStore();
const favorites = useFavoritesStore();

const q = ref("");
const categoryKeyword = ref("");
const minPrice = ref("");
const maxPrice = ref("");
const sort = ref("new");
const page = ref(1);
const pageSize = 12;
const filtersOpen = ref(false);

const debounced = useDebounce<string>(400);

const categoryOptions = [
  { value: "", label: "Все изделия" },
  { value: "шарф", label: "Шарфы" },
  { value: "вареж", label: "Варежки" },
  { value: "носк", label: "Носки" },
  { value: "кардиган", label: "Кардиганы" },
  { value: "плать", label: "Платья" },
  { value: "юбк", label: "Юбки" },
  { value: "сум", label: "Сумки" },
];

const combinedQuery = computed(() => {
  const parts = [debounced.value.value?.trim(), categoryKeyword.value.trim()].filter(Boolean);
  return parts.length ? parts.join(" ") : undefined;
});

const isEmpty = computed(() => !catalog.isLoading && catalog.products.length === 0);
const hasFilters = computed(() => Boolean(q.value || categoryKeyword.value || minPrice.value || maxPrice.value || sort.value !== "new"));

watch(q, (value) => debounced.set(value));
watch(
  () => debounced.value.value,
  () => {
    page.value = 1;
    loadCatalog();
  },
);
watch([sort, categoryKeyword], () => {
  page.value = 1;
  loadCatalog();
});

function loadCatalog() {
  catalog.fetchCatalog({
    q: combinedQuery.value,
    min_price: minPrice.value || undefined,
    max_price: maxPrice.value || undefined,
    sort: sort.value,
    page: page.value,
    page_size: pageSize,
  });
}

function applyFilters() {
  page.value = 1;
  filtersOpen.value = false;
  loadCatalog();
}

function clearFilters() {
  q.value = "";
  categoryKeyword.value = "";
  minPrice.value = "";
  maxPrice.value = "";
  sort.value = "new";
  page.value = 1;
  debounced.set("");
  loadCatalog();
}

onMounted(async () => {
  loadCatalog();

  if (auth.isAuthenticated) {
    try {
      await favorites.fetchFavorites();
    } catch {
      favorites.items = [];
    }
  }
});
</script>

<template>
  <section class="space-y-6">
    <header class="rounded-[20px] bg-[linear-gradient(135deg,rgba(255,209,228,0.85),rgba(255,210,227,0.95))] p-6 md:p-8">
      <h1 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Каталог вязаных изделий</h1>
      <p class="mt-2 text-[1.18rem] text-primary-dark/80">Шарфы, кардиганы, носки и другие уютные вещи ручной работы</p>
    </header>

    <section class="brand-card space-y-4 p-4 md:p-5">
      <div class="grid gap-3 md:grid-cols-[1fr_auto] md:items-center">
        <UiInput v-model="q" label="Поиск" placeholder="Например, кардиган, шарф или носки" aria-label="Поиск товаров" />
        <UiButton class="md:hidden" variant="secondary" @click="filtersOpen = true">Фильтры</UiButton>
      </div>

      <div class="hidden gap-3 md:grid md:grid-cols-4">
        <UiDropdown v-model="categoryKeyword" aria-label="Категория" :options="categoryOptions" />
        <UiInput v-model="minPrice" label="Мин. цена" type="number" aria-label="Минимальная цена" />
        <UiInput v-model="maxPrice" label="Макс. цена" type="number" aria-label="Максимальная цена" />
        <UiDropdown
          v-model="sort"
          aria-label="Сортировка"
          :options="[
            { value: 'new', label: 'Сначала новые' },
            { value: 'price_asc', label: 'Сначала дешевле' },
            { value: 'price_desc', label: 'Сначала дороже' },
          ]"
        />
      </div>

      <div class="hidden justify-end gap-2 md:flex">
        <UiButton v-if="hasFilters" variant="ghost" @click="clearFilters">Сбросить</UiButton>
        <UiButton @click="applyFilters">Применить</UiButton>
      </div>
    </section>

    <transition name="fade">
      <div v-if="filtersOpen" class="fixed inset-0 z-50 bg-black/40 md:hidden" @click.self="filtersOpen = false">
        <div class="brand-bottom-sheet absolute bottom-0 w-full bg-white p-4">
          <h2 class="brand-title text-3xl font-bold text-primary-dark">Фильтры</h2>
          <div class="mt-4 space-y-3">
            <UiDropdown v-model="categoryKeyword" aria-label="Категория" :options="categoryOptions" />
            <UiInput v-model="minPrice" label="Мин. цена" type="number" aria-label="Минимальная цена" />
            <UiInput v-model="maxPrice" label="Макс. цена" type="number" aria-label="Максимальная цена" />
            <UiDropdown
              v-model="sort"
              aria-label="Сортировка"
              :options="[
                { value: 'new', label: 'Сначала новые' },
                { value: 'price_asc', label: 'Сначала дешевле' },
                { value: 'price_desc', label: 'Сначала дороже' },
              ]"
            />
          </div>

          <div class="mt-4 grid grid-cols-2 gap-2">
            <UiButton variant="ghost" @click="clearFilters">Сбросить</UiButton>
            <UiButton @click="applyFilters">Показать</UiButton>
          </div>
        </div>
      </div>
    </transition>

    <UiSkeleton v-if="catalog.isLoading" :rows="6" />

    <section v-else-if="isEmpty" class="brand-empty-state p-8 text-center">
      <h3 class="brand-title text-4xl font-bold text-primary-dark">Товары не найдены</h3>
      <p class="mt-2 text-[1.14rem] text-muted">Попробуйте изменить фильтры или очистить поисковый запрос</p>
      <UiButton class="mt-4" @click="clearFilters">Сбросить фильтры</UiButton>
    </section>

    <section v-else class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <KnitProductCard v-for="item in catalog.products" :key="item.id" :product="item" />
    </section>

    <UiPagination :page="page" :page-size="pageSize" :total="catalog.total" @change="(value) => { page = value; loadCatalog(); }" />
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
