<script setup lang="ts">
withDefaults(
  defineProps<{
    tone?: "default" | "success" | "warning" | "danger";
  }>(),
  { tone: "default" },
);

const map = {
  default: "bg-brand-100 text-brand-900",
  success: "bg-emerald-100 text-emerald-800",
  warning: "bg-amber-100 text-amber-900",
  danger: "bg-red-100 text-red-800",
};
</script>

<template>
  <span class="inline-flex rounded-full px-2.5 py-1 text-xs font-bold" :class="map[tone]">
    <slot />
  </span>
</template>

