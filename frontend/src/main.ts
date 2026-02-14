import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./app/router";
import { useUiStore } from "./app/stores/ui";

import "./styles/base.css";
import "./styles/brand.css";
import "./styles/tailwind.css";

const app = createApp(App);
const pinia = createPinia();

app.config.errorHandler = (err) => {
  const ui = useUiStore(pinia);
  const message = err instanceof Error ? err.message : "Неизвестная ошибка интерфейса";
  ui.setFatalError(message);
  ui.pushToast("error", "Произошла ошибка интерфейса");
  console.error(err);
};

router.onError((err) => {
  const ui = useUiStore(pinia);
  const message = err instanceof Error ? err.message : "Ошибка маршрутизации";
  ui.setFatalError(message);
  ui.pushToast("error", "Ошибка маршрутизации");
  console.error(err);
});

app.use(pinia);
app.use(router);

app.mount("#app");

