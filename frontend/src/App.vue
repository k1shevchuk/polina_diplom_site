<template>
  <router-view />
  <UiToast />
  <UiConfirmDialog />
</template>

<script setup lang="ts">
import UiConfirmDialog from "./components/ui/UiConfirmDialog.vue";
import UiToast from "./components/ui/UiToast.vue";
</script>

