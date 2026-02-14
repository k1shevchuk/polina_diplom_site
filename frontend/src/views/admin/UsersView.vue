<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { AxiosError } from "axios";

import UiButton from "../../components/ui/UiButton.vue";
import UiInput from "../../components/ui/UiInput.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";

interface AdminRole {
  id: number;
  name: string;
}

interface AdminUser {
  id: number;
  email: string;
  is_banned: boolean;
  is_active: boolean;
  roles: AdminRole[];
  created_at: string;
}

const ui = useUiStore();
const users = ref<AdminUser[]>([]);
const search = ref("");
const isLoading = ref(false);

const filteredUsers = computed(() => {
  const q = search.value.trim().toLowerCase();
  if (!q) return users.value;
  return users.value.filter((user) => user.email.toLowerCase().includes(q));
});

function extractApiError(error: unknown): string {
  if (error instanceof AxiosError && typeof error.response?.data?.detail === "string") {
    return error.response.data.detail;
  }
  return "Ошибка админ-операции";
}

async function load() {
  isLoading.value = true;
  try {
    const response = await api.get<AdminUser[]>(endpoints.admin.users);
    users.value = response.data;
  } catch (error) {
    users.value = [];
    ui.pushToast("error", extractApiError(error));
  } finally {
    isLoading.value = false;
  }
}

function toggleBan(user: AdminUser) {
  const willBan = !user.is_banned;
  ui.askConfirm({
    title: willBan ? "Заблокировать пользователя" : "Разблокировать пользователя",
    message: willBan
      ? `Пользователь ${user.email} будет заблокирован.`
      : `Пользователь ${user.email} будет разблокирован.`,
    onConfirm: async () => {
      try {
        await api.post(`${endpoints.admin.users}/${user.id}/ban?is_banned=${willBan}`);
        ui.pushToast("success", willBan ? "Пользователь заблокирован" : "Пользователь разблокирован");
        await load();
      } catch (error) {
        ui.pushToast("error", extractApiError(error));
      }
    },
  });
}

onMounted(load);
</script>

<template>
  <section class="space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <h1 class="font-display text-2xl font-bold text-primary-dark">Пользователи</h1>
      <div class="w-full max-w-sm">
        <UiInput v-model="search" label="Поиск по email" placeholder="user@example.com" />
      </div>
    </div>

    <UiSkeleton v-if="isLoading" :rows="5" />

    <div v-else class="overflow-x-auto rounded-2xl border border-brand-200">
      <table class="w-full min-w-[760px] text-left text-sm">
        <thead class="bg-brand-50 text-primary-dark">
          <tr>
            <th class="px-3 py-2">ID</th>
            <th class="px-3 py-2">Email</th>
            <th class="px-3 py-2">Роли</th>
            <th class="px-3 py-2">Статус</th>
            <th class="px-3 py-2">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id" class="border-t">
            <td class="px-3 py-2">{{ user.id }}</td>
            <td class="px-3 py-2">{{ user.email }}</td>
            <td class="px-3 py-2">{{ user.roles.map((role) => role.name).join(", ") || "-" }}</td>
            <td class="px-3 py-2">{{ user.is_banned ? "Заблокирован" : "Активен" }}</td>
            <td class="px-3 py-2">
              <UiButton variant="secondary" @click="toggleBan(user)">
                {{ user.is_banned ? "Разбан" : "Бан" }}
              </UiButton>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
