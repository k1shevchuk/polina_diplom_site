<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { useAuthStore } from "../stores/auth";
import { useCartStore } from "../../features/cart/store";

const auth = useAuthStore();
const cartStore = useCartStore();
const route = useRoute();

const isMobileMenuOpen = ref(false);
const isScrolled = ref(false);

const accountRoute = computed(() => (auth.isAuthenticated ? "/me" : "/auth/login"));
const showSellerPanelLink = computed(() => auth.isAuthenticated && auth.hasRole("SELLER"));
const showAdminPanelLink = computed(() => auth.isAuthenticated && auth.hasRole("ADMIN"));
const cartItemsCount = computed(() => cartStore.cart?.items.reduce((acc, item) => acc + item.qty, 0) ?? 0);

function onScroll() {
  isScrolled.value = window.scrollY > 8;
}

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
}

watch(
  () => route.fullPath,
  () => {
    isMobileMenuOpen.value = false;
  },
);

watch(
  () => auth.isAuthenticated,
  async (isAuthenticated) => {
    if (isAuthenticated) {
      try {
        await cartStore.fetchCart();
      } catch {
        cartStore.cart = null;
      }
    } else {
      cartStore.cart = null;
    }
  },
  { immediate: true },
);

onMounted(() => {
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", onScroll);
});
</script>

<template>
  <header class="brand-header" :class="{ 'brand-header--scrolled': isScrolled }">
    <div class="brand-container flex items-center justify-between gap-3 px-4 py-3 md:px-0">
      <router-link to="/" class="flex items-center gap-3 text-white no-underline">
        <img src="/brand/logo.png" alt="Craft With Love" class="h-12 w-auto object-contain md:h-14" />
        <span class="font-display text-2xl font-bold leading-none md:text-[2.35rem]">Craft With Love</span>
      </router-link>

      <nav class="hidden flex-1 items-center justify-end gap-4 text-[1.02rem] font-semibold md:flex">
        <router-link class="brand-nav-link whitespace-nowrap" to="/">Главная</router-link>
        <router-link class="brand-nav-link whitespace-nowrap" to="/catalog">Каталог</router-link>
        <router-link class="brand-nav-link whitespace-nowrap" to="/about">О бренде</router-link>
        <router-link class="brand-nav-link whitespace-nowrap" to="/customers">Покупателям</router-link>
        <router-link class="brand-nav-link whitespace-nowrap" to="/favorites">Избранное</router-link>
        <router-link class="brand-nav-link relative whitespace-nowrap" to="/cart">
          Корзина
          <span v-if="cartItemsCount > 0" class="brand-cart-badge">{{ cartItemsCount }}</span>
        </router-link>
        <router-link v-if="showSellerPanelLink" class="brand-nav-link whitespace-nowrap" to="/seller/dashboard">Продавец</router-link>
        <router-link v-if="showAdminPanelLink" class="brand-nav-link whitespace-nowrap" to="/admin">Админ</router-link>
        <router-link class="brand-nav-link whitespace-nowrap" :to="accountRoute">Профиль</router-link>
      </nav>

      <button
        type="button"
        class="flex h-10 w-10 items-center justify-center rounded-full border border-white/40 bg-white/10 text-white md:hidden"
        :aria-label="isMobileMenuOpen ? 'Закрыть меню' : 'Открыть меню'"
        :aria-expanded="isMobileMenuOpen"
        @click="toggleMobileMenu"
      >
        <span class="sr-only">Меню</span>
        <div class="relative h-4 w-5">
          <span class="absolute left-0 top-0 h-0.5 w-full bg-white transition" :class="{ 'translate-y-[7px] rotate-45': isMobileMenuOpen }" />
          <span class="absolute left-0 top-[7px] h-0.5 w-full bg-white transition" :class="{ 'opacity-0': isMobileMenuOpen }" />
          <span
            class="absolute left-0 top-[14px] h-0.5 w-full bg-white transition"
            :class="{ '-translate-y-[7px] -rotate-45': isMobileMenuOpen }"
          />
        </div>
      </button>
    </div>

    <transition name="mobile-menu">
      <nav v-if="isMobileMenuOpen" class="brand-container border-t border-white/20 bg-[rgba(53,13,54,0.88)] px-4 py-4 md:hidden">
        <div class="grid gap-3 text-[1.08rem] font-semibold">
          <router-link class="brand-nav-link" to="/">Главная</router-link>
          <router-link class="brand-nav-link" to="/catalog">Каталог</router-link>
          <router-link class="brand-nav-link" to="/about">О бренде</router-link>
          <router-link class="brand-nav-link" to="/customers">Покупателям</router-link>
          <router-link class="brand-nav-link" to="/favorites">Избранное</router-link>
          <router-link class="brand-nav-link relative w-fit" to="/cart">
            Корзина
            <span v-if="cartItemsCount > 0" class="brand-cart-badge">{{ cartItemsCount }}</span>
          </router-link>
          <router-link v-if="showSellerPanelLink" class="brand-nav-link" to="/seller/dashboard">Продавец</router-link>
          <router-link v-if="showAdminPanelLink" class="brand-nav-link" to="/admin">Админ</router-link>
          <router-link class="brand-nav-link" :to="accountRoute">Профиль</router-link>
        </div>
      </nav>
    </transition>
  </header>
</template>

<style scoped>
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
