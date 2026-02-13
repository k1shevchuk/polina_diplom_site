<script setup lang="ts">
import { reactive } from "vue";
import { useRouter } from "vue-router";

import UiButton from "../../components/ui/UiButton.vue";
import UiInput from "../../components/ui/UiInput.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";

const ui = useUiStore();
const router = useRouter();

const form = reactive({
  title: "",
  description: "",
  price: "",
  stock: "",
  tags: "",
  materials: "",
  image_urls: "",
});

async function saveDraft() {
  await api.post("/seller/products", {
    title: form.title,
    description: form.description,
    price: Number(form.price),
    stock: form.stock ? Number(form.stock) : null,
    tags: form.tags.split(",").map((x) => x.trim()).filter(Boolean),
    materials: form.materials.split(",").map((x) => x.trim()).filter(Boolean),
    image_urls: form.image_urls.split(",").map((x) => x.trim()).filter(Boolean),
  });
  ui.pushToast("success", "Черновик сохранён");
  router.push("/seller/products");
}
</script>

<template>
  <section>
    <h1 class="mb-4 font-display text-2xl font-bold">Новый товар</h1>
    <form class="space-y-3" @submit.prevent="saveDraft">
      <UiInput v-model="form.title" label="Название" />
      <UiInput v-model="form.description" label="Описание" />
      <UiInput v-model="form.price" type="number" label="Цена" />
      <UiInput v-model="form.stock" type="number" label="Остаток" />
      <UiInput v-model="form.tags" label="Теги (через запятую)" />
      <UiInput v-model="form.materials" label="Материалы (через запятую)" />
      <UiInput v-model="form.image_urls" label="URL фото (через запятую)" />
      <UiButton type="submit">Сохранить черновик</UiButton>
    </form>
  </section>
</template>

