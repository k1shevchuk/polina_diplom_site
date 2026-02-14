<script setup lang="ts">
import { computed, onMounted } from "vue";

import KnitProductCard from "../../components/catalog/KnitProductCard.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useAuthStore } from "../../app/stores/auth";
import { useCatalogStore } from "../../features/catalog/store";
import { useFavoritesStore } from "../../features/favorites/store";
import { formatCurrency } from "../../shared/utils/currency";
import { getProductImage } from "../../shared/utils/product-image";
import { cleanText } from "../../shared/utils/text";

const auth = useAuthStore();
const catalog = useCatalogStore();
const favorites = useFavoritesStore();

const categories = [
  "Шарфы",
  "Варежки",
  "Носки",
  "Кардиганы",
  "Платья",
  "Юбки",
  "Сумки",
  "Свитеры",
];

const featuredProducts = computed(() => catalog.products.slice(0, 4));
const saleProducts = computed(() => catalog.products.slice(4, 8));
const topProducts = computed(() => catalog.products.slice(0, 10));
const topProductsTrack = computed(() => [...topProducts.value, ...topProducts.value]);

onMounted(async () => {
  await catalog.fetchCatalog({ sort: "popular", page: 1, page_size: 20 });
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
  <section class="space-y-14">
    <section class="brand-hero -mx-4 md:-mx-0 md:rounded-[22px]">
      <div class="brand-container brand-hero-content flex min-h-[78vh] items-center px-4 md:px-0">
        <div class="max-w-3xl py-16 md:py-20">
          <p class="font-script text-4xl text-brand-100 md:text-5xl">Craft With Love</p>
          <h1 class="brand-title mt-4 text-5xl font-bold leading-tight md:text-7xl">Связано с любовью</h1>
          <p class="mt-6 max-w-2xl text-2xl leading-relaxed text-white/95 md:text-3xl">
            Маркетплейс вязаных изделий ручной работы: уютные вещи для дома и гардероба, созданные мастерами с вниманием к каждой петле.
          </p>

          <div class="mt-8 flex flex-wrap gap-3">
            <router-link to="/catalog" class="brand-btn px-7 py-3 text-[1.25rem]">Перейти в каталог</router-link>
            <router-link to="/about" class="brand-btn brand-btn-outline px-7 py-3 text-[1.25rem]">
              О бренде
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <section class="brand-card overflow-hidden p-5 md:p-6">
      <header class="mb-4 flex items-end justify-between gap-3">
        <div>
          <h2 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Топ изделия недели</h2>
          <p class="text-[1.1rem] text-muted">Бесконечная лента хитов Craft With Love</p>
        </div>
        <router-link to="/catalog?sort=popular" class="text-[1.1rem] font-bold text-primary-dark">В каталог</router-link>
      </header>

      <UiSkeleton v-if="catalog.isLoading" :rows="2" />

      <div v-else class="overflow-hidden">
        <div class="brand-top-slider-track">
          <router-link
            v-for="(product, index) in topProductsTrack"
            :key="`top-${index}-${product.id}`"
            :to="`/product/${product.id}`"
            class="brand-top-slide"
            :aria-label="`Открыть товар ${cleanText(product.title, 'Вязаное изделие')}`"
          >
            <img
              :src="getProductImage(product)"
              :alt="cleanText(product.title, 'Вязаное изделие')"
              class="h-44 w-full rounded-xl object-cover"
              loading="lazy"
            />
            <p class="mt-3 line-clamp-1 text-xl font-semibold text-primary-dark">
              {{ cleanText(product.title, "Вязаное изделие") }}
            </p>
            <p class="mt-1 text-lg font-bold text-primary-dark">{{ formatCurrency(product.price) }}</p>
          </router-link>
        </div>
      </div>
    </section>

    <section class="brand-section py-0">
      <header class="mb-6 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Популярные товары</h2>
          <p class="text-[1.2rem] text-muted">Выбор покупателей Craft With Love</p>
        </div>
        <router-link to="/catalog" class="text-[1.15rem] font-bold text-primary-dark">Смотреть всё</router-link>
      </header>

      <UiSkeleton v-if="catalog.isLoading" :rows="4" />

      <div v-else class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <KnitProductCard v-for="product in featuredProducts" :key="product.id" :product="product" />
      </div>
    </section>

    <section class="brand-card grid gap-5 overflow-hidden p-6 md:grid-cols-[1.1fr_1fr] md:p-8">
      <div>
        <h2 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Уют и качество в каждой вещи</h2>
        <p class="mt-3 text-[1.2rem] text-muted">
          Мы собрали мастеров, которые создают вязаные изделия из натуральных материалов. От шарфов и носков до кардиганов и сумок.
        </p>
        <router-link to="/customers" class="brand-btn mt-5 px-6 py-3 text-[1.15rem]">Условия для покупателей</router-link>
      </div>
      <img
        src="/brand/about-preview.jpeg"
        alt="Вязаные изделия Craft With Love"
        class="h-full max-h-[360px] w-full rounded-2xl object-cover"
        loading="lazy"
      />
    </section>

    <section>
      <h2 class="brand-title mb-4 text-4xl font-bold text-primary-dark md:text-5xl">Категории knitwear</h2>
      <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <router-link
          v-for="category in categories"
          :key="category"
          :to="`/catalog?q=${encodeURIComponent(category.toLowerCase())}`"
          class="rounded-full border border-brand-200 bg-white px-5 py-2 text-center text-[1.12rem] font-semibold text-primary-dark transition hover:-translate-y-0.5 hover:border-brand-300 hover:bg-brand-50"
        >
          {{ category }}
        </router-link>
      </div>
    </section>

    <section>
      <header class="mb-6 flex items-end justify-between gap-4">
        <div>
          <h2 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Новые поступления</h2>
          <p class="text-[1.2rem] text-muted">Свежие работы мастеров</p>
        </div>
        <router-link to="/catalog?sort=new" class="text-[1.15rem] font-bold text-primary-dark">Новинки</router-link>
      </header>

      <UiSkeleton v-if="catalog.isLoading" :rows="4" />
      <div v-else class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <KnitProductCard v-for="product in saleProducts" :key="`new-${product.id}`" :product="product" compact />
      </div>
    </section>
  </section>
</template>

<style scoped>
.brand-top-slider-track {
  display: flex;
  width: max-content;
  gap: 1rem;
  animation: top-products-marquee 36s linear infinite;
}

.brand-top-slider-track:hover {
  animation-play-state: paused;
}

.brand-top-slide {
  width: 220px;
  flex: 0 0 auto;
  border-radius: 16px;
  background: #fff;
  padding: 0.75rem;
  text-decoration: none;
  box-shadow: var(--shadow-soft);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.brand-top-slide:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card-hover);
}

@keyframes top-products-marquee {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

@media (max-width: 768px) {
  .brand-top-slide {
    width: 180px;
  }
}
</style>
