<script setup lang="ts">
import { useRouter } from "vue-router";

import UiButton from "../../components/ui/UiButton.vue";
import { useAuthStore } from "../../app/stores/auth";
import { useUiStore } from "../../app/stores/ui";

const auth = useAuthStore();
const ui = useUiStore();
const router = useRouter();

async function becomeSeller() {
  try {
    await auth.toggleSeller(true);
    ui.pushToast("success", "Роль продавца включена");
  } catch {
    ui.pushToast("error", "Не удалось обновить роль");
  }
}

async function logout() {
  await auth.logout();
  ui.pushToast("success", "Вы вышли из аккаунта");
  router.replace("/auth/login");
}
</script>

<template>
  <section class="space-y-6">
    <header class="rounded-[20px] bg-[linear-gradient(135deg,rgba(255,209,228,0.85),rgba(255,210,227,0.95))] p-6 md:p-8">
      <h1 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Личный кабинет</h1>
      <p class="mt-2 text-[1.16rem] text-primary-dark/85">Управление профилем и ролями аккаунта</p>
    </header>

    <section class="brand-card p-6">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div class="flex items-center gap-4">
          <div class="flex h-16 w-16 items-center justify-center rounded-full bg-brand-gradient text-3xl font-bold text-white">
            {{ (auth.me?.email?.[0] || "U").toUpperCase() }}
          </div>
          <div>
            <h2 class="brand-title text-4xl font-bold text-primary-dark">{{ auth.me?.email }}</h2>
            <p class="text-[1.08rem] text-muted">Роли: {{ auth.me?.roles.join(", ") || "-" }}</p>
          </div>
        </div>

        <div class="flex flex-wrap gap-2">
          <UiButton v-if="!auth.me?.roles.includes('SELLER')" @click="becomeSeller">Стать продавцом</UiButton>
          <router-link to="/orders" class="brand-btn brand-btn-outline px-5 py-2 text-[1.02rem]">Мои заказы</router-link>
          <UiButton variant="ghost" @click="logout">Выйти</UiButton>
        </div>
      </div>
    </section>

    <section class="grid gap-4 md:grid-cols-2">
      <article class="brand-card p-5">
        <h3 class="text-3xl font-bold text-primary-dark">Покупки</h3>
        <p class="mt-2 text-[1.08rem] text-muted">Проверяйте статусы заказов, уведомления и переписку с продавцами.</p>
        <div class="mt-4 flex flex-wrap gap-2">
          <router-link to="/orders" class="brand-btn px-5 py-2 text-[1.02rem]">Заказы</router-link>
          <router-link to="/messages" class="brand-btn brand-btn-outline px-5 py-2 text-[1.02rem]">Сообщения</router-link>
        </div>
      </article>

      <article class="brand-card p-5">
        <h3 class="text-3xl font-bold text-primary-dark">Избранное и отзывы</h3>
        <p class="mt-2 text-[1.08rem] text-muted">Возвращайтесь к понравившимся товарам и оставляйте отзывы после покупки.</p>
        <div class="mt-4 flex flex-wrap gap-2">
          <router-link to="/favorites" class="brand-btn px-5 py-2 text-[1.02rem]">Избранное</router-link>
          <router-link to="/customers" class="brand-btn brand-btn-outline px-5 py-2 text-[1.02rem]">Покупателям</router-link>
        </div>
      </article>
    </section>
  </section>
</template>
