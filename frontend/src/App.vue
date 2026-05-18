<template>
  <a href="#main-content" class="skip-to-content">Skip to main content</a>
  <div id="main-content">
    <router-view :dir="appStore.isRtl ? 'rtl' : 'ltr'" />
  </div>
</template>

<script setup lang="ts">
import { watch } from 'vue';
import { useAppStore } from './stores/app';
import { useI18n } from 'vue-i18n';
import { Quasar } from 'quasar';
import langEn from 'quasar/lang/en-US'
import langAr from 'quasar/lang/ar'

const appStore = useAppStore();
const { locale } = useI18n();

watch(() => appStore.locale, (newLocale) => {
  locale.value = newLocale;
  Quasar.lang.set(newLocale === 'ar-EG' ? langAr : langEn);
}, { immediate: true });
</script>
