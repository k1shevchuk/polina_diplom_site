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
  <label class="flex flex-col gap-1 text-[1.03rem] font-semibold text-primary-dark">
    <span v-if="label">{{ label }}</span>
    <input
      :value="modelValue"
      :type="type ?? 'text'"
      :placeholder="placeholder"
      :aria-label="ariaLabel || label"
      class="brand-input px-3 py-2.5 text-[1.03rem] outline-none"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
  </label>
</template>

