<script setup lang="ts">
import BrandFooter from "./BrandFooter.vue";
import BrandHeader from "./BrandHeader.vue";
</script>

<template>
  <div class="brand-page">
    <BrandHeader />
    <main class="brand-main">
      <div class="brand-container px-4 py-8 md:px-0">
        <router-view />
      </div>
    </main>
    <BrandFooter />
  </div>
</template>
