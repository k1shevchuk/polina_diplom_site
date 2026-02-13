<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import KnitProductCard from "../../components/catalog/KnitProductCard.vue";
import UiButton from "../../components/ui/UiButton.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useAuthStore } from "../../app/stores/auth";
import { useUiStore } from "../../app/stores/ui";
import { useCartStore } from "../../features/cart/store";
import { useFavoritesStore } from "../../features/favorites/store";
import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { Product, Paginated } from "../../shared/types/product";
import type { Review } from "../../shared/types/review";
import { formatCurrency } from "../../shared/utils/currency";
import { formatDate } from "../../shared/utils/date";
import { getProductImage } from "../../shared/utils/product-image";

const route = useRoute();
const auth = useAuthStore();
const ui = useUiStore();
const cartStore = useCartStore();
const favoritesStore = useFavoritesStore();

const isLoading = ref(true);
const product = ref<Product | null>(null);
const relatedProducts = ref<Product[]>([]);
const reviews = ref<Review[]>([]);
const selectedImage = ref(0);
const activeTab = ref<"description" | "reviews" | "delivery">("description");

const productId = computed(() => Number(route.params.id));

const gallery = computed(() => {
  if (!product.value) return [];
  if (product.value.images.length > 0) return product.value.images.map((image) => image.image_url);
  return [getProductImage(product.value)];
});

const selectedImageSrc = computed(() => gallery.value[selectedImage.value] || "");
const isFavorite = computed(() => (product.value ? favoritesStore.items.includes(product.value.id) : false));
const related = computed(() => relatedProducts.value.slice(0, 4));

async function fetchProductDetail() {
  isLoading.value = true;

  try {
    const response = await api.get<Product>(`${endpoints.catalog}/${productId.value}`);
    product.value = response.data;
    selectedImage.value = 0;

    await Promise.all([fetchRelated(response.data), fetchReviews(response.data.id)]);
  } catch {
    product.value = null;
    relatedProducts.value = [];
    reviews.value = [];
  } finally {
    isLoading.value = false;
  }
}

async function fetchRelated(current: Product) {
  const response = await api.get<Paginated<Product>>(endpoints.catalog, {
    params: {
      category_id: current.category_id ?? undefined,
      sort: "new",
      page: 1,
      page_size: 8,
    },
  });

  relatedProducts.value = response.data.items.filter((item) => item.id !== current.id);
}

async function fetchReviews(id: number) {
  const response = await api.get<Review[]>(endpoints.reviewsByProduct(id));
  reviews.value = response.data.filter((item) => !item.is_hidden);
}

async function addToCart() {
  if (!product.value) return;

  if (!auth.isAuthenticated) {
    ui.pushToast("info", "Войдите, чтобы оформить заказ");
    return;
  }

  try {
    await cartStore.addItem(product.value.id, 1);
    ui.pushToast("success", "Товар добавлен в корзину");
  } catch {
    ui.pushToast("error", "Не удалось добавить товар");
  }
}

async function toggleFavorite() {
  if (!product.value) return;

  if (!auth.isAuthenticated) {
    ui.pushToast("info", "Войдите, чтобы добавить товар в избранное");
    return;
  }

  try {
    await favoritesStore.toggleFavorite(product.value.id);
    ui.pushToast("success", isFavorite.value ? "Добавлено в избранное" : "Убрано из избранного");
  } catch {
    ui.pushToast("error", "Не удалось обновить избранное");
  }
}

onMounted(async () => {
  if (auth.isAuthenticated) {
    try {
      await favoritesStore.fetchFavorites();
    } catch {
      favoritesStore.items = [];
    }
  }
  await fetchProductDetail();
});

watch(productId, () => {
  fetchProductDetail();
});
</script>

<template>
  <section class="space-y-8">
    <UiSkeleton v-if="isLoading" :rows="5" />

    <template v-else-if="product">
      <section class="rounded-2xl bg-brand-100/60 p-4 text-[1.05rem] text-muted">
        <div class="flex flex-wrap items-center gap-2">
          <router-link to="/" class="hover:text-primary-dark">Главная</router-link>
          <span>/</span>
          <router-link to="/catalog" class="hover:text-primary-dark">Каталог</router-link>
          <span>/</span>
          <span class="text-primary-dark">{{ product.title }}</span>
        </div>
      </section>

      <section class="grid gap-6 lg:grid-cols-[1.1fr_1fr]">
        <div class="space-y-3">
          <div class="overflow-hidden rounded-[20px] bg-brand-100">
            <img
              :src="selectedImageSrc"
              :srcset="`${selectedImageSrc} 960w`"
              sizes="(max-width: 768px) 100vw, 56vw"
              :alt="product.title"
              class="h-[430px] w-full object-cover md:h-[520px]"
              loading="lazy"
            />
          </div>
          <div class="grid grid-cols-4 gap-2">
            <button
              v-for="(image, index) in gallery"
              :key="`${image}-${index}`"
              type="button"
              class="overflow-hidden rounded-xl border-2 transition"
              :class="selectedImage === index ? 'border-primary' : 'border-transparent hover:border-brand-200'"
              :aria-label="`Открыть фото ${index + 1}`"
              @click="selectedImage = index"
            >
              <img :src="image" :alt="`Фото ${index + 1}`" class="h-20 w-full object-cover" loading="lazy" />
            </button>
          </div>
        </div>

        <article class="brand-card space-y-5 p-6">
          <div class="flex flex-wrap gap-2">
            <span class="rounded-full bg-brand-100 px-3 py-1 text-sm font-bold text-primary-dark">Вязаное изделие</span>
            <span class="rounded-full bg-brand-50 px-3 py-1 text-sm font-bold text-primary-dark">Ручная работа</span>
          </div>

          <h1 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">{{ product.title }}</h1>
          <p class="text-[1.2rem] text-muted">{{ product.description }}</p>

          <div class="flex items-end gap-3">
            <p class="text-4xl font-extrabold text-primary-dark">{{ formatCurrency(product.price) }}</p>
            <span class="pb-1 text-[1.08rem] text-muted">{{ product.stock ? `В наличии: ${product.stock}` : "В наличии" }}</span>
          </div>

          <div class="grid gap-3 sm:grid-cols-2">
            <UiButton class="w-full" @click="addToCart">Добавить в корзину</UiButton>
            <UiButton class="w-full" variant="secondary" @click="toggleFavorite">
              {{ isFavorite ? "Убрать из избранного" : "В избранное" }}
            </UiButton>
          </div>

          <div class="rounded-2xl bg-brand-50 p-4">
            <p class="text-[1.1rem] font-semibold text-primary-dark">Продавец #{{ product.seller_id }}</p>
            <router-link :to="`/seller/${product.seller_id}`" class="text-[1.05rem] font-semibold text-primary-dark">
              Открыть профиль продавца
            </router-link>
          </div>

          <ul class="space-y-2 text-[1.06rem] text-muted">
            <li>Бережная упаковка и отправка</li>
            <li>Оформление заказа без онлайн-оплаты</li>
            <li>Уведомления продавцу сразу после checkout</li>
          </ul>
        </article>
      </section>

      <section class="brand-card p-5 md:p-6">
        <div class="tabs-header mb-5 flex flex-wrap gap-2 border-b border-brand-100 pb-2">
          <button
            class="rounded-full px-4 py-2 text-[1.08rem] font-semibold transition"
            :class="activeTab === 'description' ? 'bg-brand-gradient text-white' : 'text-primary-dark hover:bg-brand-100'"
            type="button"
            @click="activeTab = 'description'"
          >
            Описание
          </button>
          <button
            class="rounded-full px-4 py-2 text-[1.08rem] font-semibold transition"
            :class="activeTab === 'reviews' ? 'bg-brand-gradient text-white' : 'text-primary-dark hover:bg-brand-100'"
            type="button"
            @click="activeTab = 'reviews'"
          >
            Отзывы ({{ reviews.length }})
          </button>
          <button
            class="rounded-full px-4 py-2 text-[1.08rem] font-semibold transition"
            :class="activeTab === 'delivery' ? 'bg-brand-gradient text-white' : 'text-primary-dark hover:bg-brand-100'"
            type="button"
            @click="activeTab = 'delivery'"
          >
            Доставка
          </button>
        </div>

        <div v-if="activeTab === 'description'" class="space-y-3 text-[1.12rem] text-muted">
          <p>{{ product.description }}</p>
          <p>Каждое изделие Craft With Love связано вручную и проходит проверку качества перед публикацией в каталоге.</p>
        </div>

        <div v-else-if="activeTab === 'reviews'" class="space-y-4">
          <div v-if="reviews.length === 0" class="brand-empty-state p-5 text-center">
            <p class="text-[1.08rem] text-muted">Пока нет отзывов. Будьте первым покупателем, кто поделится впечатлением.</p>
          </div>

          <article
            v-for="review in reviews"
            :key="review.id"
            class="rounded-2xl border border-brand-100 bg-white p-4"
          >
            <div class="flex items-center justify-between gap-2">
              <p class="font-semibold text-primary-dark">Покупатель #{{ review.user_id }}</p>
              <p class="text-sm text-muted">{{ formatDate(review.created_at) }}</p>
            </div>
            <p class="text-sm text-primary-dark">Оценка: {{ review.rating }}/5</p>
            <p class="mt-2 text-[1.07rem] text-muted">{{ review.text }}</p>
          </article>
        </div>

        <div v-else class="space-y-3 text-[1.12rem] text-muted">
          <p>После оформления заказа продавец получает уведомление и подтверждает детали вручную.</p>
          <p>Средний срок отправки: 1-3 дня, в зависимости от готовности изделия.</p>
          <p>Подробные условия смотрите в разделе <router-link to="/customers" class="font-semibold">Покупателям</router-link>.</p>
        </div>
      </section>

      <section class="space-y-4">
        <div class="flex items-end justify-between gap-3">
          <h2 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Похожие товары</h2>
          <router-link to="/catalog" class="text-[1.1rem] font-semibold text-primary-dark">Все товары</router-link>
        </div>

        <div v-if="related.length" class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <KnitProductCard v-for="item in related" :key="item.id" :product="item" compact />
        </div>
        <div v-else class="brand-empty-state p-6 text-center text-[1.05rem] text-muted">
          В этой категории пока нет других товаров.
        </div>
      </section>

      <div class="brand-sticky-cta fixed inset-x-4 bottom-3 z-40 p-3 md:hidden">
        <div class="flex items-center justify-between gap-3">
          <strong class="text-xl text-primary-dark">{{ formatCurrency(product.price) }}</strong>
          <div class="flex gap-2">
            <UiButton variant="secondary" @click="toggleFavorite">Избранное</UiButton>
            <UiButton @click="addToCart">Купить</UiButton>
          </div>
        </div>
      </div>
    </template>

    <section v-else class="brand-empty-state p-8 text-center">
      <h2 class="brand-title text-4xl font-bold text-primary-dark">Товар не найден</h2>
      <p class="mt-2 text-[1.1rem] text-muted">Возможно, изделие уже снято с витрины.</p>
      <router-link to="/catalog" class="brand-btn mt-4 px-6 py-3">Вернуться в каталог</router-link>
    </section>
  </section>
</template>
