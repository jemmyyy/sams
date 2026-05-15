<template>
  <q-page class="q-pa-xl animate-up">
    <!-- Player Hero Banner -->
    <div class="row q-col-gutter-lg q-mb-xl">
      <div class="col-12">
        <q-card flat class="profile-hero overflow-hidden">
           <q-card-section class="row items-center q-pa-xl bg-gradient-sport">
              <div class="col-auto">
                <div class="avatar-wrapper">
                  <q-avatar size="160px" class="profile-avatar border-primary shadow-lg">
                    <img src="https://cdn.quasar.dev/img/boy-avatar.png">
                  </q-avatar>
                  <div class="rank-badge">
                    <q-icon name="stars" size="24px" color="white" />
                    <span>ELITE</span>
                  </div>
                </div>
              </div>
              <div class="col q-ml-xl">
                <div class="text-overline text-primary letter-spacing-3 uppercase">Professional Division</div>
                <h2 class="text-heading text-white no-margin">ADAM <span class="text-secondary">SMITH</span></h2>
                <div class="row q-gutter-md q-mt-md">
                  <div class="id-pill">
                    <span class="text-grey-5">MEMBER ID:</span>
                    <span class="text-weight-bold">SAMS-2026-081</span>
                  </div>
                  <div class="id-pill">
                    <span class="text-grey-5">AGE:</span>
                    <span class="text-weight-bold">12 YEARS</span>
                  </div>
                </div>
              </div>
              <div class="col-auto gt-sm text-right">
                <div class="text-overline text-grey-5 letter-spacing-2">GLOBAL RANK</div>
                <div class="text-h2 text-weight-black text-white">#04</div>
                <q-badge color="success" class="q-px-sm">+2 pos</q-badge>
              </div>
           </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Stats Matrix -->
    <div class="row q-col-gutter-lg q-mb-xl">
      <div class="col-12 col-md-3" v-for="stat in quickStats" :key="stat.label">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="row items-center justify-between q-mb-md">
            <div class="stat-icon row items-center justify-center bg-surface-2 border-b">
               <q-icon :name="stat.icon" size="24px" :color="stat.color" />
            </div>
            <div class="text-caption text-grey-5 uppercase text-weight-bold">Active</div>
          </div>
          <div class="text-h4 text-heading text-white q-mb-xs">{{ stat.value }}</div>
          <div class="text-caption text-grey-5 uppercase text-weight-bold letter-spacing-1">{{ stat.label }}</div>
        </q-card>
      </div>
    </div>

    <div class="row q-col-gutter-xl">
      <!-- Performance Evolution -->
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sams-card full-height">
          <div class="q-pa-lg border-bottom bg-surface-2 row items-center justify-between">
             <div class="text-heading text-subtitle1 text-white uppercase letter-spacing-1">Skill Matrix Breakdown</div>
             <q-btn flat round icon="insights" color="primary" />
          </div>
          
          <q-card-section class="q-pa-xl column q-gutter-y-xl bg-surface-1">
            <div v-for="skill in skills" :key="skill.name">
              <div class="row items-center justify-between q-mb-sm">
                <div class="row items-center">
                  <q-icon :name="skill.icon" color="primary" class="q-mr-md" size="24px" />
                  <div class="text-subtitle1 text-weight-bold uppercase text-white">{{ skill.name }}</div>
                </div>
                <div class="text-h6 text-secondary text-weight-black">{{ Math.round(skill.value * 100) }}%</div>
              </div>
              <q-linear-progress 
                :value="skill.value" 
                size="12px" 
                color="primary" 
                track-color="surface-2"
                rounded
              >
                <div class="absolute-full flex flex-center">
                  <q-badge color="white" text-color="primary" :label="`${Math.round(skill.value * 100)}%`" class="transparent no-shadow" />
                </div>
              </q-linear-progress>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Achievement Timeline -->
      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card full-height">
          <div class="q-pa-lg border-bottom bg-surface-2">
             <div class="text-heading text-subtitle1 text-white uppercase letter-spacing-1">Career Milestones</div>
          </div>
          
          <q-list class="q-px-md q-py-lg" dark>
            <q-item v-for="(milestone, idx) in milestones" :key="idx" class="q-mb-md milestone-card bg-surface-2">
              <q-item-section avatar>
                <div class="milestone-icon">
                  <q-icon :name="milestone.icon" :color="milestone.color" size="md" />
                </div>
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold text-white uppercase">{{ milestone.title }}</q-item-label>
                <q-item-label caption class="text-grey-5">{{ milestone.desc }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
          
          <q-card-actions align="center" class="q-pb-lg">
            <q-btn outline color="primary" label="View Full Trophy Room" class="full-width q-mx-md sams-btn" />
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
const quickStats = [
  { label: 'Attendance', value: '92%', icon: 'fact_check', color: 'success' },
  { label: 'Avg Rating', value: '4.8', icon: 'stars', color: 'warning' },
  { label: 'Units Done', value: '142', icon: 'timer', color: 'primary' },
  { label: 'Milestones', value: '12', icon: 'emoji_events', color: 'secondary' },
];

const skills = [
  { name: 'Technique', value: 0.85, icon: 'sports_handball' },
  { name: 'Stamina', value: 0.70, icon: 'bolt' },
  { name: 'Strategy', value: 0.92, icon: 'psychology' },
  { name: 'Teamwork', value: 0.80, icon: 'groups' }
];

const milestones = [
  { title: 'Golden Grip', desc: 'Excellence in technique award.', icon: 'military_tech', color: 'warning' },
  { title: 'Iron Lung', desc: 'Completed 10 endurance sessions.', icon: 'air', color: 'info' },
  { title: 'MVP June', desc: 'Top performer in the U12 category.', icon: 'workspace_premium', color: 'secondary' }
];
</script>

<style lang="scss" scoped>
.letter-spacing-3 { letter-spacing: 3px; }
.letter-spacing-1 { letter-spacing: 1px; }

.bg-surface-1 { background-color: var(--sams-surface-1); }
.bg-surface-2 { background-color: var(--sams-surface-2); }
.border-b { border: 1px solid var(--sams-border); }
.border-bottom { border-bottom: 1px solid var(--sams-border); }

.bg-gradient-sport {
  background: linear-gradient(135deg, var(--sams-surface-2) 0%, var(--sams-bg) 100%);
  border-bottom: 1px solid var(--sams-border);
}

.profile-hero {
  border-radius: 30px;
  background-color: var(--sams-surface-1);
  border: 1px solid var(--sams-border);
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
}

.profile-avatar {
  border: 4px solid var(--sams-primary);
  box-shadow: 0 0 30px rgba(59, 130, 246, 0.3);
}

.rank-badge {
  position: absolute;
  bottom: 0;
  right: 10px;
  background: var(--sams-secondary, #ff6d00);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 800;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.id-pill {
  background: var(--sams-bg);
  padding: 8px 16px;
  border-radius: 12px;
  border: 1px solid var(--sams-border);
  font-size: 12px;
  display: flex;
  gap: 8px;
  color: white;
}

.stat-icon {
  width: 44px; height: 44px;
  border-radius: 12px;
}

.milestone-card {
  border-radius: 16px;
  border: 1px solid var(--sams-border);
  transition: all 0.3s ease;
  &:hover {
    border-color: var(--sams-primary);
    transform: translateX(5px);
  }
}

.milestone-icon {
  background: rgba(255, 255, 255, 0.05);
  padding: 10px;
  border-radius: 12px;
}
</style>
