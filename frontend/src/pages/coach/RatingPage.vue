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
      <div v-for="player in players" :key="player.id" class="col-12 col-sm-6 col-md-4">
        <q-card flat bordered class="sport-card bg-white q-pa-md hover-elevate transition-all" @click="ratePlayer(player)">
          <q-item class="q-pa-none">
            <q-item-section avatar>
              <q-avatar size="64px" class="shadow-2 border-primary">
                <img :src="`https://i.pravatar.cc/150?u=${player.id}`">
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-weight-black text-h6 text-primary">{{ player.name }}</q-item-label>
              <q-item-label caption>Current Rank: #{{ player.id }}</q-item-label>
            </q-item-section>
            <q-item-section side>
               <q-btn flat round color="secondary" icon="star_half" />
            </q-item-section>
          </q-item>

          <q-separator class="q-my-md opacity-20" />

          <div class="row items-center justify-between">
            <div class="text-caption text-weight-bold uppercase text-grey-6">Last Performance</div>
            <div class="text-h6 text-secondary text-weight-black">{{ player.lastRating }} <q-icon name="trending_up" color="positive" size="xs" /></div>
          </div>
        </q-card>
      </div>
    </div>

    <!-- Designer Rating Dialog -->
    <q-dialog v-model="showRatingDialog" transition-show="scale" transition-hide="scale">
      <q-card class="sport-card bg-white" style="min-width: 400px; border-radius: 30px">
        <div class="bg-gradient-primary text-white q-pa-xl text-center">
          <q-avatar size="100px" class="q-mb-md border-white shadow-10">
            <img :src="`https://i.pravatar.cc/150?u=${selectedPlayer?.id}`">
          </q-avatar>
          <div class="text-h4 text-weight-black uppercase">{{ selectedPlayer?.name }}</div>
          <div class="text-subtitle1 opacity-80 letter-spacing-2">PERFORMANCE EVALUATION</div>
        </div>

        <q-card-section class="q-pa-xl column q-gutter-y-lg">
          <div class="column q-gutter-y-md">
             <div class="row items-center justify-between">
               <span class="text-weight-bold uppercase">Technical Mastery</span>
               <q-rating v-model="currentRating.technique" size="2.5em" color="secondary" icon="sports_handball" />
             </div>
             <div class="row items-center justify-between">
               <span class="text-weight-bold uppercase">Stamina / Power</span>
               <q-rating v-model="currentRating.stamina" size="2.5em" color="secondary" icon="bolt" />
             </div>
             <div class="row items-center justify-between">
               <span class="text-weight-bold uppercase">Mental Strategy</span>
               <q-rating v-model="currentRating.teamwork" size="2.5em" color="secondary" icon="psychology" />
             </div>
          </div>

          <q-input v-model="currentRating.notes" type="textarea" label="Professional Observations" outlined bg-color="grey-1" class="q-mt-md" rounded-borders />
        </q-card-section>

        <q-card-actions align="center" class="q-pa-xl bg-grey-1">
          <q-btn flat label="ABORT" color="grey-6" v-close-popup class="q-px-lg" />
          <q-btn unelevated label="COMMIT RATINGS" color="primary" v-close-popup class="q-px-xl text-weight-black shadow-5" rounded size="lg" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Player {
  id: number;
  name: string;
  lastRating: string;
}

const players = ref<Player[]>([
  { id: 1, name: 'ADAM SMITH', lastRating: '4.8' },
  { id: 2, name: 'SARAH JONES', lastRating: '4.5' },
  { id: 3, name: 'MIKE BROWN', lastRating: '4.2' },
  { id: 4, name: 'EMMA WILSON', lastRating: '4.9' }
]);

const showRatingDialog = ref(false);
const selectedPlayer = ref<Player | null>(null);
const currentRating = ref({
  technique: 4,
  stamina: 3,
  teamwork: 5,
  notes: ''
});

function ratePlayer(player: Player) {
  selectedPlayer.value = player;
  showRatingDialog.value = true;
}
</script>

<style lang="scss" scoped>
.letter-spacing-1 { letter-spacing: 1px; }
.letter-spacing-2 { letter-spacing: 2px; }

.sport-card {
  border-radius: 24px;
}

.bg-gradient-primary {
  background: linear-gradient(135deg, #1a237e 0%, #0d123d 100%);
}

.border-primary { border: 2px solid $primary; }
.border-white { border: 3px solid white; }

.hover-elevate {
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.1) !important;
    border-color: $secondary;
  }
}

.opacity-20 { opacity: 0.2; }
</style>
