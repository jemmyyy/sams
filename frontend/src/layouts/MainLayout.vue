<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <router-view v-slot="{ Component }">
        <transition
          appear
          enter-active-class="animated fadeIn"
          leave-active-class="animated fadeOut"
        >
          <component :is="Component" />
        </transition>
      </router-view>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
// Main entrance layout with global transitions
</script>

<style lang="scss">
body {
  background-color: #f5f7fa;
}

.animated {
  animation-duration: 0.4s;
}
</style>
