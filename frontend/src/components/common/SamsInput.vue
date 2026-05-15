<template>
  <q-input
    v-bind="$attrs"
    outlined
    dark
    :color="color"
    :bg-color="bgColor"
    class="sams-input"
    :label-color="labelColor"
  >
    <template v-for="(_, name) in $slots" #[name]="slotData">
      <slot :name="name" v-bind="slotData || {}" />
    </template>
  </q-input>
</template>

<script setup lang="ts">
interface Props {
  color?: string;
  bgColor?: string;
  labelColor?: string;
}

withDefaults(defineProps<Props>(), {
  color: 'primary',
  bgColor: 'surface-2',
  labelColor: 'grey-5'
});
</script>

<style lang="scss" scoped>
.sams-input {
  :deep(.q-field__control) {
    border-radius: 12px;
    transition: all 0.3s ease;
    
    &:hover {
      border-color: var(--sams-primary);
    }
  }

  :deep(.q-field__label) {
    font-weight: 500;
  }
}
</style>
