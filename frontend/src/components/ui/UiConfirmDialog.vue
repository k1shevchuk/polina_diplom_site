<script setup lang="ts">
import UiButton from "./UiButton.vue";
import UiModal from "./UiModal.vue";
import { useUiStore } from "../../app/stores/ui";

const ui = useUiStore();

async function onConfirm() {
  if (!ui.confirm) return;
  await ui.confirm.onConfirm();
  ui.closeConfirm();
}
</script>

<template>
  <UiModal :open="Boolean(ui.confirm)" :title="ui.confirm?.title" @close="ui.closeConfirm">
    <p class="mb-4 text-[1.06rem] text-ink">{{ ui.confirm?.message }}</p>
    <div class="flex justify-end gap-2">
      <UiButton variant="ghost" @click="ui.closeConfirm">{{ ui.confirm?.cancelText || "Отмена" }}</UiButton>
      <UiButton variant="danger" @click="onConfirm">{{ ui.confirm?.confirmText || "Подтвердить" }}</UiButton>
    </div>
  </UiModal>
</template>
