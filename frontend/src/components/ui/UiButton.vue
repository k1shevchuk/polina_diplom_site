<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    type?: "button" | "submit" | "reset";
    variant?: "primary" | "secondary" | "danger" | "ghost";
    disabled?: boolean;
  }>(),
  { type: "button", variant: "primary", disabled: false },
);

const classes = {
  primary: "bg-brand-600 text-white hover:bg-brand-700",
  secondary: "bg-brand-100 text-brand-900 hover:bg-brand-200",
  danger: "bg-red-600 text-white hover:bg-red-700",
  ghost: "bg-transparent text-brand-700 hover:bg-brand-100",
};
</script>

<template>
  <button
    :type="props.type"
    :disabled="props.disabled"
    class="inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-bold transition disabled:cursor-not-allowed disabled:opacity-50"
    :class="classes[props.variant]"
  >
    <slot />
  </button>
</template>
