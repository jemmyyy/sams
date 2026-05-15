<template>
  <q-dialog v-bind="$attrs" backdrop-filter="blur(4px)">
    <q-card class="sams-dialog sams-card" :style="{ minWidth: width }">
      <q-card-section class="bg-surface-2 q-pa-lg border-b row items-center justify-between">
        <div class="column">
          <div class="text-h6 text-weight-bold text-white">{{ title }}</div>
          <div v-if="subtitle" class="text-caption text-grey-5">{{ subtitle }}</div>
        </div>
        <q-btn flat round dense icon="close" color="grey-5" v-close-popup />
      </q-card-section>

      <q-card-section class="q-pa-xl bg-surface-1">
        <slot />
      </q-card-section>

      <q-card-actions v-if="$slots.actions" align="right" class="q-pa-lg bg-surface-2 border-t">
        <slot name="actions" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
interface Props {
  title: string;
  subtitle?: string;
  width?: string;
}

withDefaults(defineProps<Props>(), {
  width: '500px'
});
</script>

<style lang="scss" scoped>
.sams-dialog {
  border-radius: 24px;
  overflow: hidden;
}

.bg-surface-1 { background-color: var(--sams-surface-1); }
.bg-surface-2 { background-color: var(--sams-surface-2); }
.border-b { border-bottom: 1px solid var(--sams-border); }
.border-t { border-top: 1px solid var(--sams-border); }
</style>
