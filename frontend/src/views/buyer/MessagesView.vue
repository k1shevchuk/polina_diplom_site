<script setup lang="ts">
import { onMounted, ref } from "vue";

import UiButton from "../../components/ui/UiButton.vue";
import UiInput from "../../components/ui/UiInput.vue";
import { usePolling } from "../../composables/usePolling";
import { useMessagesStore } from "../../features/messages/store";

const store = useMessagesStore();
const draft = ref("");

onMounted(async () => {
  await store.fetchConversations();
  if (store.conversations[0]) {
    await store.fetchMessages(store.conversations[0].id);
  }
});

usePolling(async () => {
  if (store.selectedConversationId) {
    await store.fetchMessages(store.selectedConversationId);
  }
}, 10000);

async function send() {
  if (!store.selectedConversationId || !draft.value.trim()) return;
  await store.sendMessage(store.selectedConversationId, draft.value.trim());
  draft.value = "";
}
</script>

<template>
  <section class="grid gap-3 md:grid-cols-[280px_1fr]">
    <aside class="rounded-2xl border border-brand-200 p-3">
      <h2 class="mb-2 font-display text-lg font-bold">Диалоги</h2>
      <button
        v-for="conversation in store.conversations"
        :key="conversation.id"
        class="mb-2 w-full rounded-xl border px-3 py-2 text-left text-sm"
        @click="store.fetchMessages(conversation.id)"
      >
        Диалог #{{ conversation.id }}
      </button>
      <p v-if="store.conversations.length === 0" class="text-sm text-ink/70">Нет сообщений</p>
    </aside>

    <div class="rounded-2xl border border-brand-200 p-3">
      <h2 class="mb-2 font-display text-lg font-bold">Сообщения</h2>
      <div class="mb-3 max-h-80 space-y-2 overflow-y-auto">
        <div v-for="message in store.messages" :key="message.id" class="rounded-xl bg-brand-50 px-3 py-2 text-sm">
          {{ message.body }}
        </div>
      </div>
      <div class="flex gap-2">
        <UiInput v-model="draft" aria-label="Текст сообщения" placeholder="Написать сообщение" />
        <UiButton @click="send">Отправить</UiButton>
      </div>
    </div>
  </section>
</template>

