<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    page: number;
    pageSize: number;
    total: number;
  }>(),
  { page: 1, pageSize: 20, total: 0 },
);
const emit = defineEmits<{ (e: "change", page: number): void }>();

const totalPages = computed(() => Math.max(1, Math.ceil(props.total / props.pageSize)));
</script>

<template>
  <div class="mt-4 flex items-center justify-center gap-3 text-sm">
    <button class="rounded border px-3 py-1" :disabled="page <= 1" @click="emit('change', page - 1)">Назад</button>
    <span>Стр. {{ page }} / {{ totalPages }}</span>
    <button class="rounded border px-3 py-1" :disabled="page >= totalPages" @click="emit('change', page + 1)">Вперёд</button>
  </div>
</template>

