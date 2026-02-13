<script setup lang="ts">
import { reactive } from "vue";
import { useRoute, useRouter } from "vue-router";

import UiButton from "../../components/ui/UiButton.vue";
import UiInput from "../../components/ui/UiInput.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";

const route = useRoute();
const router = useRouter();
const ui = useUiStore();

const form = reactive({ title: "", description: "", price: "", stock: "" });

async function save() {
  await api.put(`/seller/products/${route.params.id}`, {
    title: form.title,
    description: form.description,
    price: Number(form.price),
    stock: Number(form.stock),
  });
  ui.pushToast("success", "Товар обновлён");
  router.push("/seller/products");
}
</script>

<template>
  <section>
    <h1 class="mb-4 font-display text-2xl font-bold">Редактирование товара</h1>
    <form class="space-y-3" @submit.prevent="save">
      <UiInput v-model="form.title" label="Название" />
      <UiInput v-model="form.description" label="Описание" />
      <UiInput v-model="form.price" type="number" label="Цена" />
      <UiInput v-model="form.stock" type="number" label="Остаток" />
      <UiButton type="submit">Сохранить</UiButton>
    </form>
  </section>
</template>
