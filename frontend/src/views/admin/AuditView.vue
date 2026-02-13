<script setup lang="ts">
import { onMounted, ref } from "vue";

import UiCard from "../../components/ui/UiCard.vue";
import { api } from "../../shared/api/client";

const rows = ref<any[]>([]);

onMounted(async () => {
  const response = await api.get("/admin/audit");
  rows.value = response.data;
});
</script>

<template>
  <section>
    <h1 class="mb-4 font-display text-2xl font-bold">Audit Log</h1>
    <div v-if="rows.length === 0" class="rounded-2xl border border-dashed border-brand-300 p-6 text-center">Записей нет</div>
    <div v-else class="space-y-2">
      <UiCard v-for="row in rows" :key="row.id">
        <p class="text-sm font-semibold">{{ row.action }} ({{ row.target_type }} #{{ row.target_id || '—' }})</p>
        <p class="text-xs text-ink/70">{{ row.created_at }}</p>
      </UiCard>
    </div>
  </section>
</template>

