<template>
  <q-page class="q-pa-md">
    <div class="text-h5 q-mb-md">Player Ratings</div>
    
    <q-list bordered separator class="bg-white">
      <q-item v-for="player in players" :key="player.id" clickable @click="ratePlayer(player)">
        <q-item-section avatar>
          <q-avatar color="primary" text-white icon="person" />
        </q-item-section>
        
        <q-item-section>
          <q-item-label>{{ player.name }}</q-item-label>
          <q-item-label caption>Last Rating: {{ player.lastRating }}</q-item-label>
        </q-item-section>
        
        <q-item-section side>
          <q-icon name="star" color="orange" />
        </q-item-section>
      </q-item>
    </q-list>
    
    <!-- Rating Dialog -->
    <q-dialog v-model="showRatingDialog">
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Rate {{ selectedPlayer?.name }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="q-gutter-y-sm">
            <div>Technique: <q-rating v-model="currentRating.technique" :max="5" size="2em" /></div>
            <div>Stamina: <q-rating v-model="currentRating.stamina" :max="5" size="2em" /></div>
            <div>Teamwork: <q-rating v-model="currentRating.teamwork" :max="5" size="2em" /></div>
            <q-input v-model="currentRating.notes" type="textarea" label="Notes" outlined dense />
          </div>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Cancel" v-close-popup />
          <q-btn flat label="Save Rating" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const players = ref([
  { id: 1, name: 'Adam Smith', lastRating: '4.5' },
  { id: 2, name: 'Sarah Jones', lastRating: '4.2' }
]);

const showRatingDialog = ref(false);
const selectedPlayer = ref<any>(null);
const currentRating = ref({
  technique: 0,
  stamina: 0,
  teamwork: 0,
  notes: ''
});

function ratePlayer(player: any) {
  selectedPlayer.value = player;
  showRatingDialog.value = true;
}
</script>
