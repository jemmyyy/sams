<template>
  <q-page class="q-pa-lg">
    <!-- Player Hero Header -->
    <div class="row q-col-gutter-lg q-mb-xl">
      <div class="col-12">
        <q-card flat class="profile-hero overflow-hidden text-white shadow-10">
           <q-card-section class="row items-center q-pa-xl bg-gradient-sport">
              <div class="col-auto">
                <q-avatar size="140px" class="profile-avatar border-white">
                  <img src="https://cdn.quasar.dev/img/boy-avatar.png">
                  <q-badge floating color="secondary" padding="6px">
                    <q-icon name="stars" size="xs" />
                  </q-badge>
                </q-avatar>
              </div>
              <div class="col q-ml-xl">
                <div class="text-overline text-grey-4 letter-spacing-3 uppercase">Elite Division</div>
                <div class="text-h2 text-weight-black no-margin">Adam <span class="text-secondary">Smith</span></div>
                <div class="row q-gutter-sm q-mt-sm">
                  <q-chip dense color="white" text-color="primary" class="text-weight-bold">ID: SAMS-2026-081</q-chip>
                  <q-chip dense color="rgba(255,255,255,0.2)" text-color="white">Age: 12</q-chip>
                </div>
              </div>
              <div class="col-auto gt-sm">
                <div class="column items-center">
                  <div class="text-h2 text-weight-black">92%</div>
                  <div class="text-caption text-grey-4">ATTENDANCE</div>
                </div>
              </div>
           </q-card-section>
        </q-card>
      </div>
    </div>

    <div class="row q-col-gutter-xl">
      <!-- Skills Radar / Performance -->
      <div class="col-12 col-md-7">
        <q-card flat bordered class="sport-card bg-white full-height">
          <q-card-section class="row items-center q-pb-none">
             <div class="text-h5 text-weight-black uppercase letter-spacing-1 text-primary">
               Performance <span class="text-secondary">Metrics</span>
             </div>
             <q-space />
             <q-btn flat round icon="more_vert" />
          </q-card-section>
          
          <q-card-section class="q-pa-xl column q-gutter-y-lg">
            <div v-for="skill in skills" :key="skill.name">
              <div class="row items-center justify-between q-mb-xs">
                <div class="text-subtitle1 text-weight-bold uppercase">{{ skill.name }}</div>
                <div class="text-h6 text-secondary text-weight-black">{{ Math.round(skill.value * 100) }}%</div>
              </div>
              <q-linear-progress 
                :value="skill.value" 
                size="15px" 
                color="primary" 
                track-color="grey-2"
                rounded
                class="skill-bar"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Recent Achievements -->
      <div class="col-12 col-md-5">
        <q-card flat bordered class="sport-card bg-white full-height">
          <q-card-section>
             <div class="text-h5 text-weight-black uppercase letter-spacing-1 text-primary">
               Milestones
             </div>
          </q-card-section>
          
          <q-list class="q-px-md">
            <q-item v-for="n in 3" :key="n" class="q-mb-md achievement-item bg-grey-1">
              <q-item-section avatar>
                <q-icon name="emoji_events" color="secondary" size="md" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">Golden Grip Award</q-item-label>
                <q-item-label caption>Awarded by Coach Marco for excellence in technique.</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const skills = [
  { name: 'Technique', value: 0.85 },
  { name: 'Stamina', value: 0.70 },
  { name: 'Strategy', value: 0.92 },
  { name: 'Teamwork', value: 0.80 }
];
</script>

<style lang="scss" scoped>
.letter-spacing-3 { letter-spacing: 3px; }
.letter-spacing-1 { letter-spacing: 1px; }

.bg-gradient-sport {
  background: linear-gradient(135deg, #1a237e 0%, #0d123d 100%);
}

.profile-hero {
  border-radius: 30px;
}

.profile-avatar {
  border: 4px solid rgba(255,255,255,0.2);
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.sport-card {
  border-radius: 24px;
  border: 1px solid rgba(0,0,0,0.05);
}

.skill-bar {
  border-radius: 10px;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}

.achievement-item {
  border-radius: 16px;
  border: 1px dashed #e0e0e0;
}
</style>
