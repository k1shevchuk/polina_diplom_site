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
    await auth.register(form.email, form.password);
    ui.pushToast("success", "Регистрация завершена");
    router.push("/");
  } catch {
    ui.pushToast("error", "Не удалось зарегистрироваться");
  }
}
</script>

<template>
  <section class="mx-auto max-w-md rounded-2xl bg-white p-6 shadow-soft">
    <h1 class="font-display text-2xl font-bold">Регистрация</h1>
    <form class="mt-4 space-y-3" @submit.prevent="submit">
      <UiInput v-model="form.email" type="email" label="Email" />
      <UiInput v-model="form.password" type="password" label="Пароль" />
      <UiButton type="submit" class="w-full" :disabled="auth.isLoading">Создать аккаунт</UiButton>
    </form>
    <p class="mt-3 text-sm">Уже есть аккаунт? <router-link to="/auth/login">Вход</router-link></p>
  </section>
</template>
