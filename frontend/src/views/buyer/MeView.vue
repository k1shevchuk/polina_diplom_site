<script setup lang="ts">
import UiButton from "../../components/ui/UiButton.vue";
import { useAuthStore } from "../../app/stores/auth";
import { useUiStore } from "../../app/stores/ui";

const auth = useAuthStore();
const ui = useUiStore();

async function becomeSeller() {
  await auth.toggleSeller(true);
  ui.pushToast("success", "Роль продавца включена");
}
</script>

<template>
  <section class="space-y-3">
    <h1 class="font-display text-2xl font-bold">Мой профиль</h1>
    <p class="text-sm">Email: {{ auth.me?.email || '—' }}</p>
    <p class="text-sm">Роли: {{ auth.me?.roles.join(', ') || '—' }}</p>
    <UiButton @click="becomeSeller">Стать продавцом</UiButton>
    <UiButton variant="ghost" @click="auth.logout">Выйти</UiButton>
  </section>
</template>

