<script setup lang="ts">
defineProps<{
  modelValue: string;
  label?: string;
  type?: string;
  placeholder?: string;
  ariaLabel?: string;
}>();

const emit = defineEmits<{ (e: "update:modelValue", value: string): void }>();
</script>

<template>
  <label class="flex flex-col gap-1 text-sm font-semibold text-ink">
    <span v-if="label">{{ label }}</span>
    <input
      :value="modelValue"
      :type="type ?? 'text'"
      :placeholder="placeholder"
      :aria-label="ariaLabel || label"
      class="w-full rounded-xl border border-brand-200 bg-white px-3 py-2 text-sm outline-none transition focus:border-brand-500"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
  </label>
</template>

