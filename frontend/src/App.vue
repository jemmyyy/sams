<template>
  <router-view :dir="appStore.isRtl ? 'rtl' : 'ltr'" />
</template>

<script setup lang="ts">
import { watch } from 'vue';
import { useAppStore } from './stores/app';
import { useI18n } from 'vue-i18n';
import { Quasar } from 'quasar';

const appStore = useAppStore();
const { locale } = useI18n();

// Synchronize global states on startup and changes
watch(() => appStore.locale, (newLocale) => {
  locale.value = newLocale;
  // Dynamic Quasar Lang packs (simplified)
  Quasar.lang.set(newLocale === 'ar-EG' ? 'ar' : 'en-US');
}, { immediate: true });
</script>
