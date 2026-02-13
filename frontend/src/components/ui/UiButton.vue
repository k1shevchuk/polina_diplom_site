<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    type?: "button" | "submit" | "reset";
    variant?: "primary" | "secondary" | "danger" | "ghost";
    disabled?: boolean;
  }>(),
  { type: "button", variant: "primary", disabled: false },
);

const variantClass = computed(() => {
  if (props.variant === "secondary") return "brand-btn brand-btn-outline";
  if (props.variant === "danger")
    return "inline-flex rounded-[var(--radius-pill)] bg-red-600 text-white transition hover:bg-red-700";
  if (props.variant === "ghost")
    return "inline-flex rounded-[var(--radius-pill)] bg-transparent text-primary-dark transition hover:bg-brand-100";
  return "brand-btn";
});
</script>

<template>
  <button
    :type="props.type"
    :disabled="props.disabled"
    class="inline-flex min-h-[2.6rem] items-center justify-center gap-2 px-4 py-2 text-[1.02rem] font-bold disabled:cursor-not-allowed disabled:opacity-60"
    :class="variantClass"
  >
    <slot />
  </button>
</template>
