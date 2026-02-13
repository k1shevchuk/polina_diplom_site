import { defineStore } from "pinia";
import { ref } from "vue";

import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { Conversation, Message } from "../../shared/types/message";

export const useMessagesStore = defineStore("messages", () => {
  const conversations = ref<Conversation[]>([]);
  const messages = ref<Message[]>([]);
  const selectedConversationId = ref<number | null>(null);

  async function fetchConversations() {
    const response = await api.get<Conversation[]>(endpoints.messages.conversations);
    conversations.value = response.data;
  }

  async function fetchMessages(conversationId: number) {
    const response = await api.get<Message[]>(`${endpoints.messages.conversations}/${conversationId}`);
    messages.value = response.data;
    selectedConversationId.value = conversationId;
  }

  async function sendMessage(conversationId: number, body: string) {
    const response = await api.post<Message>(`${endpoints.messages.conversations}/${conversationId}`, { body });
    messages.value.push(response.data);
  }

  return {
    conversations,
    messages,
    selectedConversationId,
    fetchConversations,
    fetchMessages,
    sendMessage,
  };
});

