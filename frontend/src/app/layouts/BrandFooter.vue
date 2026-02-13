<template>
  <footer class="mt-16 border-t border-brand-200 bg-white/80 py-12">
    <div class="brand-container grid gap-8 px-4 md:grid-cols-[1.4fr_1fr_1fr] md:px-0">
      <section>
        <div class="mb-3 flex items-center gap-3">
          <img src="/brand/logo.png" alt="Craft With Love" class="h-12 w-12 rounded-full border border-brand-200 object-cover" />
          <p class="font-display text-3xl font-semibold text-primary-dark">Craft With Love</p>
        </div>
        <p class="text-[1.18rem] text-muted">
          Связано с любовью: уютные вязаные изделия ручной работы от мастеров, которым важны качество, тепло и детали.
        </p>
      </section>

      <section>
        <h3 class="font-display text-2xl font-semibold text-primary-dark">Покупателям</h3>
        <ul class="mt-3 space-y-2 text-[1.18rem]">
          <li><router-link to="/customers#delivery">Доставка</router-link></li>
          <li><router-link to="/customers#returns">Возврат</router-link></li>
          <li><router-link to="/customers#payment">Оформление заказа</router-link></li>
          <li><router-link to="/customers#care">Уход за изделиями</router-link></li>
        </ul>
      </section>

      <section>
        <h3 class="font-display text-2xl font-semibold text-primary-dark">Категории</h3>
        <ul class="mt-3 space-y-2 text-[1.18rem]">
          <li><router-link to="/catalog?q=шарф">Шарфы</router-link></li>
          <li><router-link to="/catalog?q=кардиган">Кардиганы</router-link></li>
          <li><router-link to="/catalog?q=носки">Носки</router-link></li>
          <li><router-link to="/catalog?q=сумка">Вязаные сумки</router-link></li>
        </ul>
      </section>
    </div>
    <div class="brand-container mt-8 border-t border-brand-100 px-4 pt-5 text-[1.04rem] text-muted md:px-0">
      © 2026 Craft With Love. Связано с любовью.
    </div>
  </footer>
</template>
