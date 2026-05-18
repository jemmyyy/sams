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
                <div class="text-overline text-primary letter-spacing-3 uppercase">{{ player?.gender || 'Athlete' }}</div>
                <h2 class="text-heading text-white no-margin">{{ player?.first_name || 'Player' }} <span class="text-secondary">{{ player?.last_name || '' }}</span></h2>
                <div class="row q-gutter-md q-mt-md">
                  <div class="id-pill">
                    <span class="text-grey-5">MEMBER ID:</span>
                    <span class="text-weight-bold">{{ memberId }}</span>
                  </div>
                  <div class="id-pill">
                    <span class="text-grey-5">AGE:</span>
                    <span class="text-weight-bold">{{ playerAge }}</span>
                  </div>
                </div>
              </div>
              <div class="col-auto gt-sm text-right">
                <div class="text-overline text-grey-5 letter-spacing-2">STATUS</div>
                <div class="text-h2 text-weight-black text-white">{{ player?.status || 'N/A' }}</div>
                <q-badge :color="player?.status === 'active' ? 'success' : 'grey'" class="q-px-sm">{{ player?.status === 'active' ? 'Active' : 'Inactive' }}</q-badge>
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
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { usePlayersStore } from '../../stores/players';
import { useRatingsStore } from '../../stores/ratings';
import { useAttendanceStore } from '../../stores/attendance';
import api from '../../api';

const authStore = useAuthStore();
const playersStore = usePlayersStore();
const ratingsStore = useRatingsStore();
const attendanceStore = useAttendanceStore();

const player = ref<any>(null);
const latestRating = ref<any>(null);
const attendanceCount = ref(0);
const attendanceRate = ref(0);

const playerName = computed(() => {
  if (!player.value) return 'Player';
  return `${player.value.first_name} ${player.value.last_name}`;
});

const memberId = computed(() => {
  if (!player.value) return '';
  return player.value.registration_number || '';
});

const playerAge = computed(() => {
  if (!player.value?.birth_date) return '';
  const age = Math.floor((Date.now() - new Date(player.value.birth_date).getTime()) / 31557600000);
  return `${age} YEARS`;
});

const quickStats = computed(() => [
  { label: 'Attendance', value: `${attendanceRate.value}%`, icon: 'fact_check', color: 'success' },
  { label: 'Avg Rating', value: latestRating.value ? String(avgRating.value) : 'N/A', icon: 'stars', color: 'warning' },
  { label: 'Units Done', value: String(attendanceCount.value), icon: 'timer', color: 'primary' },
  { label: 'Status', value: player.value?.status || 'Active', icon: 'emoji_events', color: 'secondary' },
]);

const avgRating = computed(() => {
  if (!latestRating.value) return 0;
  const r = latestRating.value;
  const scores = [r.technique, r.stamina, r.teamwork].filter((v: any) => typeof v === 'number');
  return scores.length ? (scores.reduce((a: number, b: number) => a + b, 0) / scores.length).toFixed(1) : 0;
});

const skills = computed(() => {
  if (!latestRating.value) return [];
  const r = latestRating.value;
  return [
    { name: 'Technique', value: (r.technique || 0) / 10, icon: 'sports_handball' },
    { name: 'Stamina', value: (r.stamina || 0) / 10, icon: 'bolt' },
    { name: 'Teamwork', value: (r.teamwork || 0) / 10, icon: 'groups' },
  ];
});

const milestones = computed(() => {
  const items = [];
  if (attendanceCount.value >= 10) {
    items.push({ title: 'Iron Lung', desc: `Completed ${attendanceCount.value} sessions.`, icon: 'air', color: 'info' });
  }
  if (latestRating.value) {
    items.push({ title: 'Rated', desc: 'Received coach evaluation.', icon: 'military_tech', color: 'warning' });
  }
  if (player.value?.status === 'active') {
    items.push({ title: 'Active', desc: 'Currently enrolled and training.', icon: 'workspace_premium', color: 'secondary' });
  }
  return items;
});

onMounted(async () => {
  const userId = authStore.user?.id;
  if (!userId) return;

  try {
    const playerRes = await api.get('players/', { params: { parent: userId } });
    const players = playerRes.data.results || playerRes.data;
    if (players.length) {
      player.value = players[0];

      await Promise.all([
        ratingsStore.fetchRatings(player.value.id),
        attendanceStore.fetchAttendance(),
      ]);

      const playerRatings = ratingsStore.ratings.filter(
        (r: any) => r.player === player.value.id || r.player === player.value.first_name
      );
      if (playerRatings.length) {
        latestRating.value = playerRatings[0];
      }

      const playerAttendance = attendanceStore.records.filter(
        (a: any) => a.player === player.value.id || a.player === player.value.first_name
      );
      attendanceCount.value = playerAttendance.length;
      const present = playerAttendance.filter((a: any) => a.status === 'Present' || a.status === 'present').length;
      attendanceRate.value = playerAttendance.length ? Math.round((present / playerAttendance.length) * 100) : 0;
    }
  } catch (err) {
    console.error('Failed to load profile');
  }
});
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
