import { defineStore } from "pinia";
import { ref } from "vue";

export interface ToastItem {
  id: number;
  type: "success" | "error" | "info";
  message: string;
}

export interface ConfirmPayload {
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  onConfirm: () => void | Promise<void>;
}

export const useUiStore = defineStore("ui", () => {
  const toasts = ref<ToastItem[]>([]);
  const confirm = ref<ConfirmPayload | null>(null);

  function pushToast(type: ToastItem["type"], message: string) {
    const id = Date.now() + Math.floor(Math.random() * 1000);
    toasts.value.push({ id, type, message });
    setTimeout(() => {
      toasts.value = toasts.value.filter((toast) => toast.id !== id);
    }, 3000);
  }

  function askConfirm(payload: ConfirmPayload) {
    confirm.value = payload;
  }

  function closeConfirm() {
    confirm.value = null;
  }

  return {
    toasts,
    confirm,
    pushToast,
    askConfirm,
    closeConfirm,
  };
});
