<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <div class="text-mono text-min text-grey-5 letter-spacing-2 uppercase q-mb-sm">Performance Metrics</div>
        <h4 class="text-apex heading-md no-margin text-white">
          CHAMPION <span class="text-energy-volt">RATINGS</span>
        </h4>
        <div class="text-grey-5 text-mono text-min uppercase q-mt-sm">Evaluate and refine player performance data</div>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <div v-if="playersStore.loading" class="q-pa-xl col-12 text-center">
        <q-spinner color="primary" size="3em" />
      </div>
      <div v-else v-for="player in playersStore.players" :key="player.id" class="col-12 col-sm-6 col-md-4">
        <q-card flat bordered class="sams-card q-pa-md hover-elevate transition-all" @click="ratePlayer(player)">
          <q-item class="q-pa-none">
            <q-item-section avatar>
              <q-avatar size="64px" class="shadow-2 border-primary">
                <img :src="`https://ui-avatars.com/api/?name=${player.first_name}+${player.last_name}&background=random`">
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-weight-black text-h6 text-primary">{{ player.first_name }} {{ player.last_name }}</q-item-label>
              <q-item-label caption class="text-grey-5">Reg: {{ player.registration_number }}</q-item-label>
            </q-item-section>
            <q-item-section side>
               <q-btn flat round color="secondary" icon="star_half" />
            </q-item-section>
          </q-item>

          <q-separator dark class="q-my-md opacity-20" />

          <div class="row items-center justify-between">
            <div class="text-caption text-weight-bold uppercase text-grey-6">Status</div>
            <div class="text-subtitle2 text-secondary text-weight-black">Active <q-icon name="trending_up" color="positive" size="xs" /></div>
          </div>
        </q-card>
      </div>
    </div>

    <!-- Designer Rating Dialog -->
    <q-dialog v-model="showRatingDialog" transition-show="scale" transition-hide="scale">
      <q-card class="sams-card" style="min-width: 400px; border-radius: 30px">
        <div class="bg-surface-2 text-white q-pa-xl text-center border-b">
          <q-avatar size="100px" class="q-mb-md border-primary shadow-10">
            <img :src="`https://ui-avatars.com/api/?name=${selectedPlayer?.first_name}+${selectedPlayer?.last_name}&background=random`">
          </q-avatar>
          <div class="text-h4 text-weight-black uppercase text-white">{{ selectedPlayer?.first_name }} {{ selectedPlayer?.last_name }}</div>
          <div class="text-subtitle1 text-grey-5 letter-spacing-2">PERFORMANCE EVALUATION</div>
        </div>

        <q-card-section class="q-pa-xl column q-gutter-y-lg bg-surface-1">
          <div class="column q-gutter-y-md">
             <div class="row items-center justify-between">
               <span class="text-weight-bold uppercase text-white">Technical Mastery</span>
               <q-rating v-model="currentRating.technique" size="2.5em" color="secondary" icon="sports_handball" />
             </div>
             <div class="row items-center justify-between">
               <span class="text-weight-bold uppercase text-white">Stamina / Power</span>
               <q-rating v-model="currentRating.stamina" size="2.5em" color="secondary" icon="bolt" />
             </div>
             <div class="row items-center justify-between">
               <span class="text-weight-bold uppercase text-white">Mental Strategy</span>
               <q-rating v-model="currentRating.teamwork" size="2.5em" color="secondary" icon="psychology" />
             </div>
          </div>

          <q-input v-model="currentRating.notes" type="textarea" label="Professional Observations" outlined dark bg-color="surface-2" class="q-mt-md sams-input" rounded-borders />
        </q-card-section>

        <q-card-actions align="center" class="q-pa-xl bg-surface-2 border-t">
          <q-btn flat label="ABORT" color="grey-6" v-close-popup class="q-px-lg" />
          <q-btn unelevated label="COMMIT RATINGS" color="primary" v-close-popup class="q-px-xl text-weight-black shadow-5" rounded size="lg" @click="submitRating" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { useRatingsStore } from '../../stores/ratings';
import { usePlayersStore } from '../../stores/players';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const authStore = useAuthStore();
const ratingsStore = useRatingsStore();
const playersStore = usePlayersStore();

const showRatingDialog = ref(false);
const selectedPlayer = ref<any>(null);
const currentRating = ref({
  technique: 4,
  stamina: 3,
  teamwork: 5,
  notes: ''
});

onMounted(() => {
  playersStore.fetchPlayers();
});

function ratePlayer(player: any) {
  selectedPlayer.value = player;
  // Reset or load existing
  currentRating.value = { technique: 3, stamina: 3, teamwork: 3, notes: '' };
  showRatingDialog.value = true;
}

async function submitRating() {
  if (!selectedPlayer.value) return;
  
  try {
    await ratingsStore.submitRating({
      player: selectedPlayer.value.id,
      coach: authStore.user?.id,
      ...currentRating.value
    });
    $q.notify({ type: 'positive', message: 'Rating submitted successfully' });
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Failed to submit rating' });
  }
}
</script>

<style lang="scss" scoped>
.letter-spacing-1 { letter-spacing: 1px; }
.letter-spacing-2 { letter-spacing: 2px; }

.bg-surface-1 { background-color: var(--sams-surface-1); }
.bg-surface-2 { background-color: var(--sams-surface-2); }
.border-b { border-bottom: 1px solid var(--sams-border); }
.border-t { border-top: 1px solid var(--sams-border); }

.border-primary { border: 2px solid var(--sams-primary); }
.border-white { border: 3px solid white; }

.hover-elevate {
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.4) !important;
    border-color: var(--sams-primary);
  }
}

.opacity-20 { opacity: 0.2; }
</style>
