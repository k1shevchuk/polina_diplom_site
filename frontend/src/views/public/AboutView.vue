<template>
  <section class="space-y-8">
    <section
      class="relative overflow-hidden rounded-[22px] px-6 py-16 text-white md:px-10"
      style="
        background:
          linear-gradient(135deg, rgba(198, 119, 151, 0.85), rgba(148, 111, 172, 0.75)),
          url('/brand/about-hero-bg.jpg') center/cover no-repeat;
      "
    >
      <div class="relative z-10 max-w-3xl">
        <p class="font-script text-4xl text-brand-100">Craft With Love</p>
        <h1 class="brand-title mt-2 text-5xl font-bold md:text-6xl">О бренде</h1>
        <p class="mt-4 text-2xl leading-relaxed text-white/90">
          Мы объединяем мастеров, которые создают вязаные изделия с теплом, вниманием к деталям и любовью к своему делу.
        </p>
      </div>
    </section>

    <section class="brand-card grid gap-6 p-6 md:grid-cols-[1.2fr_1fr] md:p-8">
      <div class="space-y-3 text-[1.18rem] text-muted">
        <h2 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Наша история</h2>
        <p>
          Craft With Love вырос из небольшой мастерской в маркетплейс вязаных изделий, где каждый товар проходит модерацию и
          публикуется только после проверки качества.
        </p>
        <p>
          Нам важны уют, экологичные материалы и честная коммуникация между покупателями и продавцами. Мы делаем платформу, где
          красивые вещи легко находить и заказывать.
        </p>

        <div class="mt-4 grid grid-cols-3 gap-3 text-center">
          <div class="rounded-2xl bg-brand-50 p-3">
            <p class="text-3xl font-bold text-primary-dark">5+</p>
            <p class="text-base text-muted">лет в теме</p>
          </div>
          <div class="rounded-2xl bg-brand-50 p-3">
            <p class="text-3xl font-bold text-primary-dark">1000+</p>
            <p class="text-base text-muted">довольных клиентов</p>
          </div>
          <div class="rounded-2xl bg-brand-50 p-3">
            <p class="text-3xl font-bold text-primary-dark">5000+</p>
            <p class="text-base text-muted">изделий создано</p>
          </div>
        </div>
      </div>

      <img src="/brand/about-story.jpeg" alt="История бренда Craft With Love" class="h-full max-h-[420px] w-full rounded-2xl object-cover" />
    </section>

    <section class="space-y-4">
      <h2 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Наши ценности</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <article class="brand-card p-5">
          <h3 class="text-2xl font-bold text-primary-dark">Уникальность</h3>
          <p class="mt-2 text-[1.12rem] text-muted">Каждое изделие связано вручную и не похоже на массовый фабричный товар.</p>
        </article>
        <article class="brand-card p-5">
          <h3 class="text-2xl font-bold text-primary-dark">Натуральность</h3>
          <p class="mt-2 text-[1.12rem] text-muted">Мы поддерживаем изделия из качественной шерсти, хлопка и смесовых пряж.</p>
        </article>
        <article class="brand-card p-5">
          <h3 class="text-2xl font-bold text-primary-dark">С любовью</h3>
          <p class="mt-2 text-[1.12rem] text-muted">Тепло и забота мастера в каждом стежке - это главная философия бренда.</p>
        </article>
        <article class="brand-card p-5">
          <h3 class="text-2xl font-bold text-primary-dark">Качество</h3>
          <p class="mt-2 text-[1.12rem] text-muted">Модерация каталога и отзывы покупателей помогают удерживать высокий уровень работ.</p>
        </article>
      </div>
    </section>
  </section>
</template>
