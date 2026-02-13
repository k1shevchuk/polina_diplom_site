<template>
  <div class="min-h-screen bg-canvas">
    <div class="mx-auto grid max-w-7xl grid-cols-1 gap-4 px-4 py-4 md:grid-cols-[260px_1fr] md:px-6">
      <aside class="rounded-2xl bg-white p-4 shadow-soft">
        <h2 class="mb-3 font-display text-lg font-bold">Админ</h2>
        <nav class="space-y-2 text-sm">
          <router-link class="block" to="/admin">Обзор</router-link>
          <router-link class="block" to="/admin/users">Пользователи</router-link>
          <router-link class="block" to="/admin/products">Товары</router-link>
          <router-link class="block" to="/admin/moderation/products">Модерация</router-link>
          <router-link class="block" to="/admin/reviews">Отзывы</router-link>
          <router-link class="block" to="/admin/stats">Статистика</router-link>
          <router-link class="block" to="/admin/audit">Аудит</router-link>
        </nav>
      </aside>
      <section class="rounded-2xl bg-white p-4 shadow-soft md:p-6">
        <router-view />
      </section>
    </div>
  </div>
</template>
