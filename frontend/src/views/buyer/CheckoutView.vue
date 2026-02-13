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
  const result = await checkoutStore.checkout(form);
  ui.pushToast("success", `Заказ оформлен: ${result.total_orders} шт.`);
  router.push("/orders");
}
</script>

<template>
  <section>
    <h1 class="mb-4 font-display text-2xl font-bold">Оформление заказа</h1>
    <form class="space-y-3" @submit.prevent="submit">
      <UiInput v-model="form.full_name" label="ФИО" />
      <UiInput v-model="form.phone" label="Телефон" />
      <UiInput v-model="form.address" label="Адрес" />
      <UiInput v-model="form.comment" label="Комментарий" />
      <UiButton type="submit" :disabled="checkoutStore.isLoading">Оформить</UiButton>
    </form>
  </section>
</template>

