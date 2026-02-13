<script setup lang="ts">
import { reactive } from "vue";
import { useRouter } from "vue-router";

import UiButton from "../../components/ui/UiButton.vue";
import UiInput from "../../components/ui/UiInput.vue";
import { useUiStore } from "../../app/stores/ui";
import { useCheckoutStore } from "../../features/checkout/store";

const checkoutStore = useCheckoutStore();
const ui = useUiStore();
const router = useRouter();

const form = reactive({
  full_name: "",
  phone: "",
  address: "",
  comment: "",
});

async function submit() {
  try {
    const result = await checkoutStore.checkout(form);
    ui.pushToast("success", `Заказ оформлен: ${result.total_orders} шт.`);
    router.push("/orders");
  } catch {
    ui.pushToast("error", "Не удалось оформить заказ");
  }
}
</script>

<template>
  <section class="space-y-6">
    <header class="rounded-[20px] bg-[linear-gradient(135deg,rgba(255,209,228,0.85),rgba(255,210,227,0.95))] p-6 md:p-8">
      <h1 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Оформление заказа</h1>
      <p class="mt-2 text-[1.15rem] text-primary-dark/85">Заполните контактные данные для подтверждения</p>
    </header>

    <form class="brand-card space-y-3 p-6" @submit.prevent="submit">
      <UiInput v-model="form.full_name" label="ФИО" aria-label="ФИО" />
      <UiInput v-model="form.phone" label="Телефон" aria-label="Телефон" />
      <UiInput v-model="form.address" label="Адрес" aria-label="Адрес" />
      <UiInput v-model="form.comment" label="Комментарий" aria-label="Комментарий" />
      <UiButton type="submit" :disabled="checkoutStore.isLoading">Оформить</UiButton>
    </form>
  </section>
</template>
