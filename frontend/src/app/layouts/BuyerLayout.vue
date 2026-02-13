<script setup lang="ts">
import BrandFooter from "./BrandFooter.vue";
import BrandHeader from "./BrandHeader.vue";
</script>

<template>
  <div class="brand-page">
    <BrandHeader />
    <main class="brand-main">
      <div class="brand-container px-4 py-8 md:px-0">
        <nav class="mb-6 flex flex-wrap gap-2 rounded-2xl border border-brand-100 bg-white/90 p-3 text-[1.15rem] shadow-soft">
          <router-link
            class="rounded-full px-4 py-1.5 text-primary-dark transition hover:bg-brand-100"
            active-class="bg-brand-gradient text-white"
            to="/orders"
          >
            Мои заказы
          </router-link>
          <router-link
            class="rounded-full px-4 py-1.5 text-primary-dark transition hover:bg-brand-100"
            active-class="bg-brand-gradient text-white"
            to="/favorites"
          >
            Избранное
          </router-link>
          <router-link
            class="rounded-full px-4 py-1.5 text-primary-dark transition hover:bg-brand-100"
            active-class="bg-brand-gradient text-white"
            to="/messages"
          >
            Сообщения
          </router-link>
          <router-link
            class="rounded-full px-4 py-1.5 text-primary-dark transition hover:bg-brand-100"
            active-class="bg-brand-gradient text-white"
            to="/notifications"
          >
            Уведомления
          </router-link>
          <router-link
            class="rounded-full px-4 py-1.5 text-primary-dark transition hover:bg-brand-100"
            active-class="bg-brand-gradient text-white"
            to="/me"
          >
            Профиль
          </router-link>
        </nav>

        <router-view />
      </div>
    </main>
    <BrandFooter />
  </div>
</template>
