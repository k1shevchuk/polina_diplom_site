<script setup lang="ts">
import UiCard from "../../components/ui/UiCard.vue";

const categories = [
  "Украшения",
  "Керамика",
  "Текстиль",
  "Декор",
  "Игрушки",
  "Аксессуары",
];

const picks = [
  { title: "Новые поступления", subtitle: "Свежие работы мастеров" },
  { title: "Популярное", subtitle: "Товары с высоким спросом" },
];
</script>

<template>
  <section class="space-y-8">
    <div class="rounded-3xl bg-gradient-to-r from-brand-700 to-brand-500 p-8 text-white shadow-soft">
      <h1 class="font-display text-3xl font-extrabold">Маркетплейс изделий ручной работы</h1>
      <p class="mt-3 max-w-2xl text-sm md:text-base">
        Находите уникальные вещи от независимых мастеров и оформляйте заказ без сложных шагов.
      </p>
      <router-link
        to="/catalog"
        class="mt-5 inline-flex rounded-xl bg-white px-4 py-2 text-sm font-bold text-brand-700"
      >
        Перейти в каталог
      </router-link>
    </div>

    <div>
      <h2 class="mb-4 font-display text-2xl font-bold">Категории</h2>
      <div class="grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-6">
        <UiCard v-for="item in categories" :key="item">
          <p class="text-sm font-bold">{{ item }}</p>
        </UiCard>
      </div>
    </div>

    <div>
      <h2 class="mb-4 font-display text-2xl font-bold">Подборки</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <UiCard v-for="pick in picks" :key="pick.title">
          <h3 class="font-display text-xl font-bold">{{ pick.title }}</h3>
          <p class="text-sm text-ink/70">{{ pick.subtitle }}</p>
        </UiCard>
      </div>
    </div>
  </section>
</template>

