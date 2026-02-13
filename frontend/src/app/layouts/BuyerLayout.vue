<template>
  <div class="min-h-screen bg-canvas">
    <div class="mx-auto grid max-w-7xl grid-cols-1 gap-4 px-4 py-4 md:grid-cols-[220px_1fr] md:px-6">
      <aside class="rounded-2xl bg-white p-4 shadow-soft">
        <h2 class="mb-3 font-display text-lg font-bold">Покупатель</h2>
        <nav class="space-y-2 text-sm">
          <router-link class="block" to="/orders">Мои заказы</router-link>
          <router-link class="block" to="/favorites">Избранное</router-link>
          <router-link class="block" to="/messages">Сообщения</router-link>
          <router-link class="block" to="/notifications">Уведомления</router-link>
          <router-link class="block" to="/me">Профиль</router-link>
        </nav>
      </aside>
      <section class="rounded-2xl bg-white p-4 shadow-soft md:p-6">
        <router-view />
      </section>
    </div>
  </div>
</template>

