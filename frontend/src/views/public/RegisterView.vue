<script setup lang="ts">
import { reactive } from "vue";
import { useRouter } from "vue-router";

import UiButton from "../../components/ui/UiButton.vue";
import UiInput from "../../components/ui/UiInput.vue";
import { useAuthStore } from "../../app/stores/auth";
import { useUiStore } from "../../app/stores/ui";

const form = reactive({ email: "", password: "", confirmPassword: "" });
const auth = useAuthStore();
const ui = useUiStore();
const router = useRouter();

async function submit() {
  if (form.password !== form.confirmPassword) {
    ui.pushToast("error", "Пароли не совпадают");
    return;
  }

  try {
    await auth.register(form.email, form.password);
    ui.pushToast("success", "Регистрация завершена");
    router.push("/");
  } catch {
    ui.pushToast("error", "Не удалось зарегистрироваться");
  }
}
</script>

<template>
  <section class="mx-auto max-w-xl space-y-6">
    <header class="rounded-[20px] bg-[linear-gradient(135deg,rgba(255,209,228,0.85),rgba(255,210,227,0.95))] p-6 text-center md:p-8">
      <h1 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Регистрация</h1>
      <p class="mt-2 text-[1.15rem] text-primary-dark/85">Создайте профиль в Craft With Love</p>
    </header>

    <form class="brand-card space-y-4 p-6" @submit.prevent="submit">
      <UiInput v-model="form.email" type="email" label="Email" aria-label="Email" />
      <UiInput v-model="form.password" type="password" label="Пароль" aria-label="Пароль" />
      <UiInput v-model="form.confirmPassword" type="password" label="Повторите пароль" aria-label="Повторите пароль" />
      <UiButton type="submit" class="w-full" :disabled="auth.isLoading">Создать аккаунт</UiButton>
    </form>

    <p class="text-center text-[1.08rem] text-muted">
      Уже есть аккаунт?
      <router-link to="/auth/login" class="font-bold text-primary-dark">Войти</router-link>
    </p>
  </section>
</template>
