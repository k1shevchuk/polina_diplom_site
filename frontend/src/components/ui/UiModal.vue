<script setup lang="ts">
defineProps<{ open: boolean; title?: string }>();
const emit = defineEmits<{ (e: "close"): void }>();
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" @click.self="emit('close')">
      <div class="w-full max-w-lg rounded-2xl bg-white p-6 shadow-soft">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="font-display text-lg font-bold">{{ title }}</h3>
          <button aria-label="Закрыть" class="rounded p-1 text-xl" @click="emit('close')">&times;</button>
        </div>
        <slot />
      </div>
    </div>
  </Teleport>
</template>

