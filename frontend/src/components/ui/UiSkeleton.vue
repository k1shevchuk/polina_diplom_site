<script setup lang="ts">
defineProps<{ rows?: number }>();
</script>

<template>
  <div class="animate-pulse space-y-3">
    <div
      v-for="idx in rows || 3"
      :key="idx"
      class="h-20 rounded-2xl bg-gradient-to-r from-brand-100 via-brand-50 to-brand-100"
    />
  </div>
</template>
