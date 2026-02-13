<script setup lang="ts">
defineProps<{ open: boolean; title?: string }>();
const emit = defineEmits<{ (e: "close"): void }>();
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center bg-black/45 p-4" @click.self="emit('close')">
      <div class="brand-card w-full max-w-lg p-6">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="font-display text-2xl font-bold text-primary-dark">{{ title }}</h3>
          <button aria-label="Закрыть" class="rounded p-1 text-xl text-primary-dark" @click="emit('close')">&times;</button>
        </div>
        <slot />
      </div>
    </div>
  </Teleport>
</template>
