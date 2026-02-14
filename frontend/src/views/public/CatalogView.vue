<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

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

const PRICE_MIN = 500;
const PRICE_MAX = 12000;
const PRICE_STEP = 100;

const auth = useAuthStore();
const catalog = useCatalogStore();
const favorites = useFavoritesStore();
const route = useRoute();
const router = useRouter();

const q = ref("");
const categoryKeyword = ref("");
const minPrice = ref(PRICE_MIN);
const maxPrice = ref(PRICE_MAX);
const sort = ref("new");
const page = ref(1);
const pageSize = 12;
const filtersOpen = ref(false);
const syncingRouteState = ref(false);

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
  { value: "свитер", label: "Свитеры" },
];

const sortOptions = [
  { value: "new", label: "Сначала новые" },
  { value: "price_asc", label: "Сначала дешевле" },
  { value: "price_desc", label: "Сначала дороже" },
];

const combinedQuery = computed(() => {
  const parts = [debounced.value.value?.trim(), categoryKeyword.value.trim()].filter(Boolean);
  return parts.length ? parts.join(" ") : undefined;
});

const isEmpty = computed(() => !catalog.isLoading && catalog.products.length === 0);
const hasFilters = computed(
  () =>
    Boolean(
      q.value ||
        categoryKeyword.value ||
        sort.value !== "new" ||
        minPrice.value !== PRICE_MIN ||
        maxPrice.value !== PRICE_MAX,
    ),
);

function clampPrice(value: number, fallback: number) {
  if (!Number.isFinite(value)) return fallback;
  return Math.min(Math.max(value, PRICE_MIN), PRICE_MAX);
}

function syncFromRouteQuery() {
  syncingRouteState.value = true;

  q.value = typeof route.query.q === "string" ? route.query.q : "";
  categoryKeyword.value = typeof route.query.category === "string" ? route.query.category : "";
  sort.value = typeof route.query.sort === "string" ? route.query.sort : "new";

  const minPriceQuery = typeof route.query.min_price === "string" ? Number(route.query.min_price) : PRICE_MIN;
  const maxPriceQuery = typeof route.query.max_price === "string" ? Number(route.query.max_price) : PRICE_MAX;
  minPrice.value = clampPrice(minPriceQuery, PRICE_MIN);
  maxPrice.value = clampPrice(maxPriceQuery, PRICE_MAX);

  if (minPrice.value > maxPrice.value) {
    const fallbackMiddle = Math.floor((minPrice.value + maxPrice.value) / 2);
    minPrice.value = clampPrice(fallbackMiddle, PRICE_MIN);
    maxPrice.value = clampPrice(fallbackMiddle, PRICE_MAX);
  }

  const pageQuery = typeof route.query.page === "string" ? Number(route.query.page) : 1;
  page.value = Number.isFinite(pageQuery) && pageQuery > 0 ? pageQuery : 1;

  debounced.set(q.value);
  syncingRouteState.value = false;
}

function updateRouteQuery() {
  const query: Record<string, string> = {};

  if (q.value.trim()) query.q = q.value.trim();
  if (categoryKeyword.value.trim()) query.category = categoryKeyword.value.trim();
  if (sort.value !== "new") query.sort = sort.value;
  if (minPrice.value > PRICE_MIN) query.min_price = String(minPrice.value);
  if (maxPrice.value < PRICE_MAX) query.max_price = String(maxPrice.value);
  if (page.value > 1) query.page = String(page.value);

  router.replace({ query }).catch(() => void 0);
}

watch(
  () => route.query,
  () => {
    syncFromRouteQuery();
    loadCatalog();
  },
  { immediate: true },
);

watch(q, (value) => debounced.set(value));
watch(
  () => debounced.value.value,
  () => {
    if (syncingRouteState.value) return;
    page.value = 1;
    updateRouteQuery();
  },
);

watch(minPrice, (value) => {
  if (value > maxPrice.value) {
    maxPrice.value = value;
  }
});

watch(maxPrice, (value) => {
  if (value < minPrice.value) {
    minPrice.value = value;
  }
});

watch([sort, categoryKeyword, minPrice, maxPrice], () => {
  if (syncingRouteState.value) return;
  page.value = 1;
  updateRouteQuery();
});

function loadCatalog() {
  catalog.fetchCatalog({
    q: combinedQuery.value,
    min_price: minPrice.value > PRICE_MIN ? minPrice.value : undefined,
    max_price: maxPrice.value < PRICE_MAX ? maxPrice.value : undefined,
    sort: sort.value,
    page: page.value,
    page_size: pageSize,
  });
}

function applyFilters() {
  page.value = 1;
  filtersOpen.value = false;
  updateRouteQuery();
}

function clearFilters() {
  q.value = "";
  categoryKeyword.value = "";
  minPrice.value = PRICE_MIN;
  maxPrice.value = PRICE_MAX;
  sort.value = "new";
  page.value = 1;
  debounced.set("");
  updateRouteQuery();
}

onMounted(async () => {
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

      <div class="hidden gap-3 md:grid md:grid-cols-2">
        <UiDropdown v-model="categoryKeyword" aria-label="Категория" :options="categoryOptions" />
        <UiDropdown v-model="sort" aria-label="Сортировка" :options="sortOptions" />
      </div>

      <div class="hidden rounded-2xl border border-brand-200 bg-brand-50/60 p-4 md:block">
        <div class="flex items-center justify-between gap-3 text-[1.02rem] font-semibold text-primary-dark">
          <span>Диапазон цены</span>
          <span>{{ minPrice }} ₽ - {{ maxPrice }} ₽</span>
        </div>
        <div class="mt-3 grid gap-3 md:grid-cols-2">
          <label class="space-y-1 text-sm font-semibold text-primary-dark">
            <span>От {{ minPrice }} ₽</span>
            <input
              v-model.number="minPrice"
              class="brand-range"
              type="range"
              :min="PRICE_MIN"
              :max="PRICE_MAX"
              :step="PRICE_STEP"
              aria-label="Минимальная цена"
            />
          </label>
          <label class="space-y-1 text-sm font-semibold text-primary-dark">
            <span>До {{ maxPrice }} ₽</span>
            <input
              v-model.number="maxPrice"
              class="brand-range"
              type="range"
              :min="PRICE_MIN"
              :max="PRICE_MAX"
              :step="PRICE_STEP"
              aria-label="Максимальная цена"
            />
          </label>
        </div>
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
            <UiDropdown v-model="sort" aria-label="Сортировка" :options="sortOptions" />

            <div class="rounded-2xl border border-brand-200 bg-brand-50/70 p-3">
              <div class="flex items-center justify-between text-sm font-semibold text-primary-dark">
                <span>Цена</span>
                <span>{{ minPrice }} ₽ - {{ maxPrice }} ₽</span>
              </div>
              <label class="mt-3 block text-xs font-semibold uppercase tracking-wide text-primary-dark/80">
                От {{ minPrice }} ₽
              </label>
              <input
                v-model.number="minPrice"
                class="brand-range mt-1"
                type="range"
                :min="PRICE_MIN"
                :max="PRICE_MAX"
                :step="PRICE_STEP"
                aria-label="Минимальная цена"
              />

              <label class="mt-3 block text-xs font-semibold uppercase tracking-wide text-primary-dark/80">
                До {{ maxPrice }} ₽
              </label>
              <input
                v-model.number="maxPrice"
                class="brand-range mt-1"
                type="range"
                :min="PRICE_MIN"
                :max="PRICE_MAX"
                :step="PRICE_STEP"
                aria-label="Максимальная цена"
              />
            </div>
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

    <UiPagination :page="page" :page-size="pageSize" :total="catalog.total" @change="(value) => { page = value; updateRouteQuery(); }" />
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

.brand-range {
  width: 100%;
  accent-color: var(--color-primary);
}
</style>
