<script setup lang="ts">
import { computed, onMounted } from "vue";

import UiButton from "../../components/ui/UiButton.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useUiStore } from "../../app/stores/ui";
import { useCartStore } from "../../features/cart/store";
import { formatCurrency } from "../../shared/utils/currency";

const cartStore = useCartStore();
const ui = useUiStore();

const fallbacks = [
  "/brand/products/scarf1.jpg",
  "/brand/products/mittens1.jpg",
  "/brand/products/socks1.jpg",
  "/brand/products/cardigan1.jpg",
  "/brand/products/dress1.jpg",
  "/brand/products/skirt1.jpg",
  "/brand/products/bag1.jpg",
  "/brand/products/sweater1.jpg",
];

const deliveryFee = computed(() => (cartStore.cart?.items.length ? 500 : 0));
const grandTotal = computed(() => Number(cartStore.cart?.total_amount ?? 0) + deliveryFee.value);

function fallbackImage(productId: number) {
  return fallbacks[productId % fallbacks.length];
}

function removeItem(id: number) {
  ui.askConfirm({
    title: "Удалить товар",
    message: "Товар будет удалён из корзины.",
    confirmText: "Удалить",
    onConfirm: async () => {
      await cartStore.removeItem(id);
      ui.pushToast("success", "Товар удалён из корзины");
    },
  });
}

onMounted(() => {
  cartStore.fetchCart();
});
</script>

<template>
  <section class="space-y-6">
    <header class="rounded-[20px] bg-[linear-gradient(135deg,rgba(255,209,228,0.85),rgba(255,210,227,0.95))] p-6 md:p-8">
      <h1 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Ваша корзина</h1>
      <p class="mt-2 text-[1.16rem] text-primary-dark/85">Проверьте состав заказа перед оформлением</p>
    </header>

    <UiSkeleton v-if="cartStore.isLoading" :rows="4" />

    <section v-else-if="!cartStore.cart || cartStore.cart.items.length === 0" class="brand-empty-state p-8 text-center">
      <h2 class="brand-title text-4xl font-bold text-primary-dark">Корзина пуста</h2>
      <p class="mt-2 text-[1.12rem] text-muted">Добавьте вязаные изделия из каталога, чтобы оформить заказ.</p>
      <router-link to="/catalog" class="brand-btn mt-4 px-6 py-3">Перейти в каталог</router-link>
    </section>

    <section v-else class="grid gap-5 lg:grid-cols-[1fr_340px]">
      <div class="space-y-3">
        <article
          v-for="item in cartStore.cart.items"
          :key="item.id"
          class="brand-card grid gap-4 p-4 sm:grid-cols-[96px_1fr_auto] sm:items-center"
        >
          <img
            :src="fallbackImage(item.product_id)"
            :alt="item.title"
            class="h-24 w-24 rounded-xl object-cover"
            loading="lazy"
          />

          <div>
            <h3 class="text-2xl font-bold text-primary-dark">{{ item.title }}</h3>
            <p class="text-[1.04rem] text-muted">{{ item.qty }} x {{ formatCurrency(item.price) }}</p>
            <p class="text-[1.02rem] text-muted">Продавец #{{ item.seller_id }}</p>
          </div>

          <div class="flex flex-col items-end gap-2">
            <strong class="text-2xl text-primary-dark">{{ formatCurrency(Number(item.price) * item.qty) }}</strong>
            <UiButton variant="danger" @click="removeItem(item.id)">Удалить</UiButton>
          </div>
        </article>
      </div>

      <aside class="brand-card h-fit space-y-3 p-5">
        <h3 class="brand-title text-3xl font-bold text-primary-dark">Итоги заказа</h3>
        <div class="space-y-2 text-[1.08rem] text-muted">
          <div class="flex items-center justify-between">
            <span>Товары</span>
            <span>{{ formatCurrency(cartStore.cart.total_amount) }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span>Доставка</span>
            <span>{{ formatCurrency(deliveryFee) }}</span>
          </div>
          <div class="flex items-center justify-between border-t border-brand-100 pt-2 text-primary-dark">
            <strong>Итого</strong>
            <strong>{{ formatCurrency(grandTotal) }}</strong>
          </div>
        </div>

        <router-link to="/checkout" class="brand-btn flex w-full px-6 py-3 text-center text-[1.12rem]">Оформить заказ</router-link>
      </aside>
    </section>
  </section>
</template>
