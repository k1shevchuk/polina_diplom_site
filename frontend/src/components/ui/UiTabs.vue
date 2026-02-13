<script setup lang="ts">
defineProps<{ tabs: Array<{ key: string; label: string }>; modelValue: string }>();
const emit = defineEmits<{ (e: "update:modelValue", value: string): void }>();
</script>

<template>
  <div class="inline-flex rounded-xl bg-brand-100 p-1" role="tablist">
    <button
      v-for="tab in tabs"
      :key="tab.key"
      role="tab"
      :aria-selected="modelValue === tab.key"
      class="rounded-lg px-3 py-1.5 text-sm font-semibold transition"
      :class="modelValue === tab.key ? 'bg-white text-brand-800 shadow' : 'text-brand-700'"
      @click="emit('update:modelValue', tab.key)"
    >
      {{ tab.label }}
    </button>
  </div>
</template>

