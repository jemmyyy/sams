<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <div class="text-mono text-min text-grey-5 letter-spacing-2 uppercase q-mb-sm">Performance Logs</div>
        <h4 class="text-apex heading-md no-margin text-white">
          SESSION <span class="text-energy-volt">REPORT</span>
        </h4>
        <div class="text-grey-5 text-mono text-min uppercase q-mt-sm">Document performance and training milestones</div>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sams-card overflow-hidden">
          <div class="bg-surface-2 text-white q-pa-lg border-b">
             <div class="text-h6 text-weight-bold">PERFORMANCE ANALYSIS</div>
             <div class="text-caption text-grey-5">Submit detailed insights for operations review</div>
          </div>

          <q-card-section class="q-pa-xl q-gutter-y-lg bg-surface-1">
            <q-input v-model="report.summary" type="textarea" label="Training Overview" outlined dark color="primary" bg-color="surface-2" class="sams-input" />
            <q-input v-model="report.achievements" type="textarea" label="Key Player Successes" outlined dark color="secondary" bg-color="surface-2" class="sams-input" />
            <q-input v-model="report.challenges" type="textarea" label="Technical Bottlenecks" outlined dark color="accent" bg-color="surface-2" class="sams-input" />
            <q-input v-model="report.next_steps" type="textarea" label="Next Session Strategy" outlined dark color="positive" bg-color="surface-2" class="sams-input" />
          </q-card-section>

          <q-card-actions class="q-pa-lg bg-surface-2 border-t">
            <q-btn flat color="grey-6" label="SAVE DRAFT" class="q-px-lg" />
            <q-space />
            <q-btn color="secondary" label="SUBMIT COMMAND" icon-right="send" size="lg" class="q-px-xl text-weight-black shadow-5" />
          </q-card-actions>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card q-pa-md">
           <div class="text-h6 text-weight-black q-mb-md text-primary uppercase">Quick Checklist</div>
           <q-list class="q-gutter-y-sm">
             <q-item tag="label" v-ripple class="bg-surface-2 rounded-borders border-b">
               <q-item-section avatar><q-checkbox v-model="checklist.att" color="secondary" dark /></q-item-section>
               <q-item-section><q-item-label class="text-white">Attendance finalized?</q-item-label></q-item-section>
             </q-item>
             <q-item tag="label" v-ripple class="bg-surface-2 rounded-borders border-b">
               <q-item-section avatar><q-checkbox v-model="checklist.ratings" color="secondary" dark /></q-item-section>
               <q-item-section><q-item-label class="text-white">Individual ratings given?</q-item-label></q-item-section>
             </q-item>
             <q-item tag="label" v-ripple class="bg-surface-2 rounded-borders border-b">
               <q-item-section avatar><q-checkbox v-model="checklist.equ" color="secondary" dark /></q-item-section>
               <q-item-section><q-item-label class="text-white">Equipment verified?</q-item-label></q-item-section>
             </q-item>
           </q-list>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const report = ref({
  summary: '',
  achievements: '',
  challenges: '',
  next_steps: ''
});

const checklist = ref({
  att: true,
  ratings: false,
  equ: true
});
</script>

<style lang="scss" scoped>
.letter-spacing-1 { letter-spacing: 1px; }

.bg-surface-1 { background-color: var(--sams-surface-1); }
.bg-surface-2 { background-color: var(--sams-surface-2); }
.border-b { border-bottom: 1px solid var(--sams-border); }
.border-t { border-top: 1px solid var(--sams-border); }

.sams-input {
  :deep(.q-field__control) {
    border-radius: 16px;
  }
}
</style>
