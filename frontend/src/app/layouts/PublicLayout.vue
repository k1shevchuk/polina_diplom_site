<script setup lang="ts">
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-[#fff4df] to-canvas">
    <header class="border-b border-brand-200 bg-white/90 backdrop-blur">
      <div class="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-3 md:px-6">
        <router-link to="/" class="font-display text-xl font-extrabold text-brand-800">Handmade Market</router-link>
        <nav class="flex items-center gap-4 text-sm font-semibold">
          <router-link to="/catalog">Каталог</router-link>
          <router-link to="/favorites">Избранное</router-link>
          <router-link to="/cart">Корзина</router-link>
          <router-link to="/messages">Сообщения</router-link>
          <router-link to="/me">Профиль</router-link>
          <router-link v-if="!auth.isAuthenticated" to="/auth/login">Войти</router-link>
        </nav>
      </div>
    </header>

    <main class="mx-auto w-full max-w-7xl px-4 py-6 md:px-6">
      <router-view />
    </main>
  </div>
</template>
