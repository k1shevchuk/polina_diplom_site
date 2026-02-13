<script setup lang="ts">
import { onMounted } from "vue";

import UiButton from "../../components/ui/UiButton.vue";
import UiCard from "../../components/ui/UiCard.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useUiStore } from "../../app/stores/ui";
import { useCartStore } from "../../features/cart/store";
import { formatCurrency } from "../../shared/utils/currency";

const store = useCartStore();
const ui = useUiStore();

onMounted(() => {
  store.fetchCart();
});

function removeItem(id: number) {
  ui.askConfirm({
    title: "Удалить товар",
    message: "Товар будет удалён из корзины.",
    confirmText: "Удалить",
    onConfirm: async () => {
      await store.removeItem(id);
      ui.pushToast("success", "Товар удалён из корзины");
    },
  });
}
</script>

<template>
  <section>
    <h1 class="mb-4 font-display text-2xl font-bold">Корзина</h1>
    <UiSkeleton v-if="store.isLoading" :rows="3" />

    <div v-else-if="!store.cart || store.cart.items.length === 0" class="rounded-2xl border border-dashed border-brand-300 p-6 text-center">
      <h2 class="font-display text-xl font-bold">Корзина пуста</h2>
      <p class="mt-1 text-sm text-ink/70">Добавьте товары из каталога, чтобы оформить заказ.</p>
      <router-link to="/catalog" class="mt-3 inline-block text-sm font-semibold">Открыть каталог</router-link>
    </div>

    <div v-else class="space-y-3">
      <UiCard v-for="item in store.cart.items" :key="item.id" class="flex items-center justify-between">
        <div>
          <h3 class="font-semibold">{{ item.title }}</h3>
          <p class="text-sm text-ink/70">{{ item.qty }} x {{ formatCurrency(item.price) }}</p>
        </div>
        <div class="flex items-center gap-3">
          <strong>{{ formatCurrency(Number(item.price) * item.qty) }}</strong>
          <UiButton variant="danger" @click="removeItem(item.id)">Удалить</UiButton>
        </div>
      </UiCard>

      <div class="flex items-center justify-between rounded-2xl bg-brand-50 p-4">
        <strong>Итого: {{ formatCurrency(store.cart.total_amount) }}</strong>
        <router-link to="/checkout" class="rounded-xl bg-brand-600 px-4 py-2 text-sm font-bold text-white">Перейти к оформлению</router-link>
      </div>
    </div>
  </section>
</template>
