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

<style lang="scss">
.auth-bg {
  background: #0d123d; // Solid fallback
  background: linear-gradient(135deg, #0d123d 0%, #1a237e 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
