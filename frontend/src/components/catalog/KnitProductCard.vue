<script setup lang="ts">
import { computed } from "vue";

import { useAuthStore } from "../../app/stores/auth";
import { useUiStore } from "../../app/stores/ui";
import { useCartStore } from "../../features/cart/store";
import { useFavoritesStore } from "../../features/favorites/store";
import type { Product } from "../../shared/types/product";
import { formatCurrency } from "../../shared/utils/currency";
import { getProductImage } from "../../shared/utils/product-image";
import { cleanText } from "../../shared/utils/text";

const props = withDefaults(
  defineProps<{
    product: Product;
    compact?: boolean;
    showActions?: boolean;
  }>(),
  { compact: false, showActions: true },
);

const auth = useAuthStore();
const cartStore = useCartStore();
const favoritesStore = useFavoritesStore();
const ui = useUiStore();

const imageSrc = computed(() => getProductImage(props.product));
const isFavorite = computed(() => favoritesStore.items.includes(props.product.id));
const displayTitle = computed(() => cleanText(props.product.title, "Вязаное изделие"));
const displayDescription = computed(() => cleanText(props.product.description, "Описание временно недоступно."));

async function toggleFavorite() {
  if (!auth.isAuthenticated) {
    ui.pushToast("info", "Войдите, чтобы добавить товар в избранное");
    return;
  }

  try {
    await favoritesStore.toggleFavorite(props.product.id);
    ui.pushToast("success", isFavorite.value ? "Товар добавлен в избранное" : "Товар удалён из избранного");
  } catch {
    ui.pushToast("error", "Не удалось обновить избранное");
  }
}

async function addToCart() {
  if (!auth.isAuthenticated) {
    ui.pushToast("info", "Войдите, чтобы добавить товар в корзину");
    return;
  }

  try {
    await cartStore.addItem(props.product.id, 1);
    ui.pushToast("success", "Товар добавлен в корзину");
  } catch {
    ui.pushToast("error", "Не удалось добавить товар в корзину");
  }
}
</script>

<template>
  <article class="brand-product-card">
    <div class="brand-product-image relative">
      <img
        :src="imageSrc"
        :srcset="`${imageSrc} 640w`"
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        :alt="displayTitle"
        class="h-56 w-full object-cover transition duration-300 hover:scale-[1.02]"
        loading="lazy"
      />

      <div class="absolute right-3 top-3 flex gap-2">
        <button
          class="brand-icon-button brand-icon-button--light"
          :class="{ '!bg-primary !text-white': isFavorite }"
          type="button"
          :aria-label="isFavorite ? 'Убрать из избранного' : 'Добавить в избранное'"
          @click="toggleFavorite"
        >
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="currentColor" aria-hidden="true">
            <path
              d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5A4.5 4.5 0 0 1 6.5 4 4.98 4.98 0 0 1 12 7.09 4.98 4.98 0 0 1 17.5 4 4.5 4.5 0 0 1 22 8.5c0 3.78-3.4 6.86-8.55 11.54z"
            />
          </svg>
        </button>
        <button
          v-if="showActions"
          class="brand-icon-button brand-icon-button--gradient"
          type="button"
          aria-label="Добавить в корзину"
          @click="addToCart"
        >
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="currentColor" aria-hidden="true">
            <path
              d="M7 18c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm10 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM7.2 14h9.94c.75 0 1.41-.41 1.75-1.03L22 6.5H6.21L5.27 4H2v2h2l3.6 7.59-1.35 2.44A1.98 1.98 0 0 0 6 17.5c0 1.1.9 2 2 2h12v-2H8.42a.25.25 0 0 1-.22-.37z"
            />
          </svg>
        </button>
      </div>

      <span class="absolute left-3 top-3 rounded-full bg-white/90 px-3 py-1 text-xs font-bold text-primary-dark">
        Вязаное изделие
      </span>
    </div>

    <div class="space-y-3 p-4">
      <router-link :to="`/product/${product.id}`" class="block font-display text-2xl font-semibold text-primary-dark">
        {{ displayTitle }}
      </router-link>
      <p v-if="!compact" class="line-clamp-2 text-base text-muted">{{ displayDescription }}</p>
      <div class="flex items-center justify-between">
        <strong class="text-2xl text-primary-dark">{{ formatCurrency(product.price) }}</strong>
        <router-link :to="`/product/${product.id}`" class="text-base font-semibold text-primary-dark">
          Подробнее
        </router-link>
      </div>
    </div>
  </article>
</template>
