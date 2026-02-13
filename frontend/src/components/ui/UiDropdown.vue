<script setup lang="ts">
defineProps<{
  modelValue: string;
  options: Array<{ value: string; label: string }>;
  ariaLabel?: string;
}>();
const emit = defineEmits<{ (e: "update:modelValue", value: string): void }>();
</script>

<template>
  <select
    :value="modelValue"
    :aria-label="ariaLabel"
    class="rounded-xl border border-brand-200 bg-white px-3 py-2 text-sm"
    @change="emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
  >
    <option v-for="option in options" :key="option.value" :value="option.value">{{ option.label }}</option>
  </select>
</template>
