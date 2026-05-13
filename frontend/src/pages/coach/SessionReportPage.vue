<template>
  <q-page class="q-pa-md">
    <div class="text-h5 q-mb-md">Submit Session Report</div>
    
    <q-card flat bordered>
      <q-card-section>
        <div class="text-subtitle1">Elite Juniors - Today</div>
      </q-card-section>
      
      <q-card-section class="q-gutter-y-md">
        <q-input v-model="report.summary" type="textarea" label="Session Summary" outlined />
        <q-input v-model="report.achievements" type="textarea" label="Key Achievements" outlined />
        <q-input v-model="report.challenges" type="textarea" label="Challenges Faced" outlined />
        <q-input v-model="report.next_steps" type="textarea" label="Next Steps" outlined />
      </q-card-section>
      
      <q-card-actions align="right">
        <q-btn color="secondary" label="Submit Report" />
      </q-card-actions>
    </q-card>
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
</script>
