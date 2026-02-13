<script setup lang="ts">
import { useUiStore } from "../../app/stores/ui";

const ui = useUiStore();

function toastColor(type: "success" | "error" | "info") {
  if (type === "success") return "bg-emerald-600";
  if (type === "error") return "bg-red-600";
  return "bg-primary-dark";
}
</script>

<template>
  <div class="pointer-events-none fixed bottom-4 right-4 z-50 flex w-full max-w-sm flex-col gap-2">
    <div
      v-for="toast in ui.toasts"
      :key="toast.id"
      class="pointer-events-auto rounded-2xl border border-white/20 px-4 py-3 text-[1.02rem] font-semibold text-white shadow-soft"
      :class="toastColor(toast.type)"
      role="status"
      aria-live="polite"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

