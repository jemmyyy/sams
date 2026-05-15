<template>
  <q-page class="ops-portal q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <div class="text-overline text-info text-weight-bolder letter-spacing-2">OPERATIONS COMMAND</div>
        <h1 class="text-h3 text-white text-weight-black q-my-none">Command Center</h1>
        <p class="text-grey-4 q-mt-sm">Monitor academy performance and logistics</p>
      </div>
      <div class="col-auto">
        <q-btn color="info" icon="add" label="Quick Action" rounded class="q-px-lg shadow-10" />
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <!-- High-Energy KPI Cards -->
      <div class="col-12 col-md-3" v-for="stat in quickStats" :key="stat.label">
        <q-card flat class="stat-card glass-card text-white">
          <q-card-section class="q-pb-none">
            <div class="text-overline text-grey-4">{{ stat.label }}</div>
            <div class="text-h4 text-weight-bold q-my-sm">{{ stat.value }}</div>
          </q-card-section>
          <q-card-section class="q-pt-none row items-center">
            <q-icon :name="stat.trendIcon" :color="stat.trendColor" size="20px" class="q-mr-xs" />
            <span :class="`text-caption text-weight-medium text-${stat.trendColor}`">{{ stat.trend }}</span>
            <q-space />
            <q-icon :name="stat.icon" size="32px" color="info" style="opacity: 0.3" />
          </q-card-section>
          <div class="progress-bar" :style="{ background: stat.color }"></div>
        </q-card>
      </div>

      <!-- Live Monitoring -->
      <div class="col-12 col-md-8">
        <q-card flat class="main-card glass-card text-white overflow-hidden">
          <q-card-section class="row items-center q-pb-md border-bottom">
            <div class="text-h6 text-weight-bold">Live Enrollment Trends</div>
            <q-space />
            <q-tabs v-model="tab" dense no-caps class="text-info" indicator-color="info">
              <q-tab name="weekly" label="Weekly" />
              <q-tab name="monthly" label="Monthly" />
            </q-tabs>
          </q-card-section>
          <q-card-section class="flex flex-center" style="height: 350px">
            <div class="text-center">
              <q-icon name="analytics" size="80px" color="info" class="q-mb-md opacity-20" />
              <div class="text-h5 text-weight-light text-grey-5 italic">Generating Real-time Data...</div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat class="side-card glass-card text-white overflow-hidden">
          <q-card-section class="q-pb-md border-bottom">
            <div class="text-h6 text-weight-bold">Recent Alerts</div>
          </q-card-section>
          <q-list dark padding separator>
            <q-item v-for="alert in alerts" :key="alert.id">
              <q-item-section avatar>
                <q-avatar :color="alert.color" size="40px" font-size="20px" :icon="alert.icon" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">{{ alert.title }}</q-item-label>
                <q-item-label caption class="text-grey-4">{{ alert.time }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
          <q-card-actions align="center" class="q-pb-md">
            <q-btn flat color="info" label="View All Operations Logs" no-caps />
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const tab = ref('weekly');

const quickStats = [
  { label: 'GROSS REVENUE', value: '124.5K', trend: '+14%', trendIcon: 'trending_up', trendColor: 'positive', icon: 'payments', color: '#00e5ff' },
  { label: 'ACTIVE ROSTER', value: '412', trend: '+8%', trendIcon: 'trending_up', trendColor: 'positive', icon: 'groups', color: '#76ff03' },
  { label: 'STAFF STATUS', value: '98%', trend: 'OPTIMAL', trendIcon: 'check_circle', trendColor: 'info', icon: 'badge', color: '#2979ff' },
  { label: 'REVENUE CHURN', value: '1.2%', trend: '-0.4%', trendIcon: 'trending_down', trendColor: 'positive', icon: 'money_off', color: '#ff1744' },
];

const alerts = [
  { id: 1, title: 'Venue Booking Overlap', time: '12 mins ago', icon: 'warning', color: 'negative' },
  { id: 2, title: 'Coach Mohamed - Report Pending', time: '1 hour ago', icon: 'pending_actions', color: 'warning' },
  { id: 3, title: 'New Registration: Ahmed Salah', time: '2 hours ago', icon: 'person_add', color: 'positive' },
  { id: 4, title: 'Payment Batch Processed', time: '4 hours ago', icon: 'done_all', color: 'info' },
];
</script>

<style lang="scss" scoped>
.ops-portal {
  background: #0a0e2e;
  min-height: 100vh;
}

.letter-spacing-2 { letter-spacing: 2px; }

.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transform: translateY(-5px);
  }
}

.stat-card {
  position: relative;
  overflow: hidden;
  .progress-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 4px;
    width: 60%;
    border-radius: 0 4px 4px 0;
    opacity: 0.7;
  }
}

.border-bottom {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.opacity-20 { opacity: 0.2; }
</style>
