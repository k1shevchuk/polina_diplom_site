<script setup lang="ts">
import { onMounted, ref } from "vue";

import UiButton from "../../components/ui/UiButton.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";

const ui = useUiStore();
const users = ref<any[]>([]);
const isLoading = ref(false);

async function load() {
  isLoading.value = true;
  try {
    const response = await api.get("/admin/users");
    users.value = response.data;
  } finally {
    isLoading.value = false;
  }
}

async function toggleBan(user: any) {
  await api.post(`/admin/users/${user.id}/ban?is_banned=${!user.is_banned}`);
  ui.pushToast("success", user.is_banned ? "Пользователь разблокирован" : "Пользователь заблокирован");
  load();
}

onMounted(load);
</script>

<template>
  <section>
    <h1 class="mb-4 font-display text-2xl font-bold">Пользователи</h1>

    <UiSkeleton v-if="isLoading" :rows="5" />

    <div v-else class="overflow-x-auto rounded-2xl border border-brand-200">
      <table class="w-full min-w-[640px] text-left text-sm">
        <thead class="bg-brand-50">
          <tr>
            <th class="px-3 py-2">ID</th>
            <th class="px-3 py-2">Email</th>
            <th class="px-3 py-2">Роли</th>
            <th class="px-3 py-2">Статус</th>
            <th class="px-3 py-2">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" class="border-t">
            <td class="px-3 py-2">{{ user.id }}</td>
            <td class="px-3 py-2">{{ user.email }}</td>
            <td class="px-3 py-2">{{ user.roles.map((r: any) => r.name).join(', ') }}</td>
            <td class="px-3 py-2">{{ user.is_banned ? 'Заблокирован' : 'Активен' }}</td>
            <td class="px-3 py-2">
              <UiButton size="sm" variant="secondary" @click="toggleBan(user)">{{ user.is_banned ? "Разбан" : "Бан" }}</UiButton>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

