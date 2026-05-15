<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
// Basic layout for auth pages to maintain full-screen focus
</script>

<style lang="scss" scoped>
.auth-bg {
  background: var(--sams-deep-bg);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
