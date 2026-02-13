<template>
  <section class="space-y-6">
    <header class="rounded-[20px] bg-[linear-gradient(135deg,rgba(255,209,228,0.85),rgba(255,210,227,0.95))] p-6 md:p-8">
      <h1 class="brand-title text-4xl font-bold text-primary-dark md:text-5xl">Покупателям</h1>
      <p class="mt-2 text-[1.18rem] text-primary-dark/85">Всё о доставке, возврате, оформлении заказа и уходе за изделиями.</p>
    </header>

    <section class="space-y-4">
      <article id="delivery" class="brand-card scroll-mt-32 p-6">
        <h2 class="brand-title text-4xl font-bold text-primary-dark">Доставка</h2>
        <p class="mt-2 text-[1.12rem] text-muted">После оформления заказа продавец получает уведомление и подтверждает детали вручную.</p>
        <ul class="mt-3 list-disc space-y-1 pl-6 text-[1.08rem] text-muted">
          <li>Курьерская доставка: 1-3 рабочих дня.</li>
          <li>Отправка по России: сроки зависят от региона.</li>
          <li>Для заказов от 5000 ₽ часто доступна бесплатная доставка у продавца.</li>
        </ul>
      </article>

      <article id="returns" class="brand-card scroll-mt-32 p-6">
        <h2 class="brand-title text-4xl font-bold text-primary-dark">Возврат</h2>
        <p class="mt-2 text-[1.12rem] text-muted">Если товар не подошёл, вы можете согласовать возврат с продавцом через сообщения и заказ.</p>
        <ul class="mt-3 list-disc space-y-1 pl-6 text-[1.08rem] text-muted">
          <li>Рекомендуемый срок обращения: до 14 дней с момента получения.</li>
          <li>Изделие должно сохранить товарный вид и комплектацию.</li>
          <li>Все договорённости фиксируются в переписке внутри платформы.</li>
        </ul>
      </article>

      <article id="payment" class="brand-card scroll-mt-32 p-6">
        <h2 class="brand-title text-4xl font-bold text-primary-dark">Оформление заказа</h2>
        <p class="mt-2 text-[1.12rem] text-muted">
          В MVP нет онлайн-оплаты: checkout создаёт один или несколько заказов (split по продавцам) и отправляет уведомления.
        </p>
        <ul class="mt-3 list-disc space-y-1 pl-6 text-[1.08rem] text-muted">
          <li>Укажите ФИО, телефон и адрес в форме checkout.</li>
          <li>Если товары от разных продавцов, система создаст несколько заказов автоматически.</li>
          <li>Статус каждого заказа отслеживается в личном кабинете.</li>
        </ul>
      </article>

      <article id="care" class="brand-card scroll-mt-32 p-6">
        <h2 class="brand-title text-4xl font-bold text-primary-dark">Уход за вязаными изделиями</h2>
        <ul class="mt-3 list-disc space-y-1 pl-6 text-[1.08rem] text-muted">
          <li>Ручная стирка до 30°C с мягким средством.</li>
          <li>Не выкручивать; аккуратно промокнуть полотенцем.</li>
          <li>Сушить на горизонтальной поверхности вдали от батарей.</li>
          <li>Хранить в сложенном виде, чтобы избежать деформации.</li>
        </ul>
      </article>
    </section>
  </section>
</template>
