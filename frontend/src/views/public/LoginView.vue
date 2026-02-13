<script setup lang="ts">
import { reactive } from "vue";
import { useRouter } from "vue-router";

import UiButton from "../../components/ui/UiButton.vue";
import UiInput from "../../components/ui/UiInput.vue";
import { useAuthStore } from "../../app/stores/auth";
import { useUiStore } from "../../app/stores/ui";

const form = reactive({ email: "", password: "" });
const auth = useAuthStore();
const ui = useUiStore();
const router = useRouter();

async function submit() {
  try {
    await auth.login(form.email, form.password);
    ui.pushToast("success", "Вход выполнен");
    router.push("/");
  } catch {
    ui.pushToast("error", "Не удалось войти");
  }
}
</script>

<template>
  <section class="mx-auto max-w-md rounded-2xl bg-white p-6 shadow-soft">
    <h1 class="font-display text-2xl font-bold">Вход</h1>
    <form class="mt-4 space-y-3" @submit.prevent="submit">
      <UiInput v-model="form.email" type="email" label="Email" aria-label="Email" />
      <UiInput v-model="form.password" type="password" label="Пароль" aria-label="Пароль" />
      <UiButton type="submit" class="w-full" :disabled="auth.isLoading">Войти</UiButton>
    </form>
    <p class="mt-3 text-sm">Нет аккаунта? <router-link to="/auth/register">Регистрация</router-link></p>
  </section>
</template>


