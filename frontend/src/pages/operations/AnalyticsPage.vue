<template>
  <q-page class="q-pa-lg">
    <div class="row items-center q-mb-xl">
      <div class="col">
        <h1 class="text-h4 text-weight-bold q-my-none">Academy Analytics</h1>
        <p class="text-grey-7 q-mt-sm">Real-time insights and performance metrics</p>
      </div>
      <div class="col-auto">
        <q-btn-group rounded outline>
          <q-btn outline label="Last 7 Days" />
          <q-btn color="dark" label="Last 30 Days" />
          <q-btn outline label="Custom" />
        </q-btn-group>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <!-- KPI Cards -->
      <div class="col-12 col-md-3" v-for="stat in quickStats" :key="stat.label">
        <q-card flat bordered class="stat-card">
          <q-card-section>
            <div class="text-overline text-grey-6">{{ stat.label }}</div>
            <div class="text-h4 text-weight-bold q-my-sm">{{ stat.value }}</div>
            <div :class="`text-caption text-weight-medium ${stat.trendColor}`">
              <q-icon :name="stat.trendIcon" /> {{ stat.trend }}
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Charts Row -->
      <div class="col-12 col-md-8">
        <q-card flat bordered class="chart-card">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6 text-weight-bold">Revenue Trends</div>
            <q-space />
            <q-btn flat round dense icon="more_vert" />
          </q-card-section>
          <q-card-section class="flex flex-center" style="height: 350px">
            <div class="text-grey-5">
              <q-icon name="insights" size="64px" class="q-mb-md block" />
              Chart Visualization Placeholder
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat bordered class="chart-card">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6 text-weight-bold">Attendance Rate</div>
            <q-space />
          </q-card-section>
          <q-card-section class="flex flex-center" style="height: 350px">
            <q-knob
              readonly
              v-model="attendanceRate"
              size="150px"
              :thickness="0.15"
              color="info"
              track-color="grey-3"
              class="q-ma-md"
              show-value
            >
              {{ attendanceRate }}%
            </q-knob>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const attendanceRate = ref(84);

const quickStats = [
  { label: 'NET REVENUE', value: '42,500 EGP', trend: '+12.5%', trendIcon: 'trending_up', trendColor: 'text-positive' },
  { label: 'ACTIVE PLAYERS', value: '156', trend: '+4.2%', trendIcon: 'trending_up', trendColor: 'text-positive' },
  { label: 'CHURN RATE', value: '2.1%', trend: '-0.5%', trendIcon: 'trending_down', trendColor: 'text-positive' },
  { label: 'UTILIZATION', value: '78%', trend: '+8.1%', trendIcon: 'trending_up', trendColor: 'text-positive' },
];
</script>

<style lang="scss" scoped>
.stat-card {
  border-radius: 16px;
  transition: transform 0.3s ease;
  &:hover {
    transform: translateY(-4px);
  }
}
.chart-card {
  border-radius: 20px;
}
</style>
