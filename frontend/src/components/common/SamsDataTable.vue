<template>
  <q-table
    v-bind="$attrs"
    flat
    dark
    class="sams-data-table"
    :table-class="'bg-surface-1 border-b'"
    :virtual-scroll="virtualScroll"
  >
    <!-- Forward all slots -->
    <template v-for="(_, name) in $slots" #[name]="slotData">
      <slot :name="name" v-bind="slotData || {}" />
    </template>

    <!-- Custom default header style -->
    <template #header="props">
      <q-tr :props="props" class="bg-surface-2">
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
          class="text-grey-5 text-weight-bold uppercase letter-spacing-1"
          style="font-size: 11px"
        >
          {{ col.label }}
        </q-th>
      </q-tr>
    </template>
  </q-table>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  virtualScroll?: boolean;
}>(), {
  virtualScroll: false,
});
</script>

<style lang="scss" scoped>
.sams-data-table {
  background: var(--sams-bg);
  border-radius: var(--sams-radius);
  overflow: hidden;

  :deep(.q-table__card) {
    box-shadow: none;
    background: transparent;
  }

  :deep(tbody tr) {
    transition: background 0.2s ease;
    height: 64px;
    
    &:hover {
      background: rgba(255, 255, 255, 0.02);
    }
  }

  :deep(tbody td) {
    border-bottom: 1px solid var(--sams-border);
    color: var(--sams-text-primary);
  }

  :deep(.q-table__bottom) {
    border-top: 1px solid var(--sams-border);
    background: var(--sams-surface-1);
    color: var(--sams-text-secondary);
  }
}

.border-b {
  border: 1px solid var(--sams-border);
}
</style>
