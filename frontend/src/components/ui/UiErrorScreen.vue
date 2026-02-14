<script setup lang="ts">
import UiButton from "./UiButton.vue";
import { useUiStore } from "../../app/stores/ui";

const ui = useUiStore();

function reloadPage() {
  ui.clearFatalError();
  window.location.reload();
}
</script>

<template>
  <section class="mx-auto max-w-3xl rounded-[20px] bg-white p-8 text-center shadow-soft">
    <h1 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Что-то пошло не так</h1>
    <p class="mt-3 text-[1.12rem] text-muted">
      {{ ui.fatalError || "Произошла ошибка интерфейса. Попробуйте обновить страницу." }}
    </p>
    <UiButton class="mt-5" @click="reloadPage">Обновить страницу</UiButton>
  </section>
</template>
