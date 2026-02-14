<template>
  <UiErrorScreen v-if="ui.fatalError" />
  <router-view v-else />
  <UiToast />
  <UiConfirmDialog />
</template>

<script setup lang="ts">
import { useUiStore } from "./app/stores/ui";
import UiConfirmDialog from "./components/ui/UiConfirmDialog.vue";
import UiErrorScreen from "./components/ui/UiErrorScreen.vue";
import UiToast from "./components/ui/UiToast.vue";

const ui = useUiStore();
</script>

