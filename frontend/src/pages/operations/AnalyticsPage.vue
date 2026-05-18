<template>
  <q-page class="q-pa-xl animate-up">
    <div class="row items-center justify-between q-mb-xl">
      <div class="column">
        <h1 class="text-heading heading-lg no-margin text-white">Performance Intelligence</h1>
        <div class="text-subtitle1 text-grey-5">Advanced metrics and enrollment trends.</div>
      </div>
      <div class="row q-gutter-md">
         <q-btn flat unelevated class="sams-btn sams-btn-primary" label="Export Raw Data" icon="download" />
      </div>
    </div>

    <!-- Analytics KPI Grid -->
    <div class="row q-col-gutter-lg q-mb-xl">
      <div class="col-12 col-md-3" v-for="stat in analyticsStats" :key="stat.label">
        <q-card flat bordered class="sams-card q-pa-lg">
          <div class="text-caption text-grey-5 uppercase text-weight-bold letter-spacing-1 q-mb-xs">{{ stat.label }}</div>
          <div class="text-h4 text-heading text-white">{{ stat.value }}</div>
          <div :class="`text-caption q-mt-sm ${stat.positive ? 'text-positive' : 'text-negative'}`">
            <q-icon :name="stat.positive ? 'trending_up' : 'trending_down'" /> {{ stat.trend }} vs last period
          </div>
        </q-card>
      </div>
    </div>

    <!-- Chart Section -->
    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-8">
        <q-card flat bordered class="sams-card bg-surface-1 q-pa-xl" style="min-height: 450px">
           <div class="text-heading text-h6 q-mb-xl text-white">Revenue Stream (MTD)</div>
           <div v-if="revenueChartData" style="height: 350px">
              <Line :data="revenueChartData" :options="chartOptions" />
           </div>
           <div v-else class="flex flex-center column q-gutter-y-md opacity-20">
              <q-icon name="insights" size="80px" color="primary" />
              <div class="text-h6 text-weight-light text-white">No revenue data yet</div>
           </div>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat bordered class="sams-card bg-surface-1 q-pa-xl" style="min-height: 450px">
           <div class="text-heading text-h6 q-mb-xl text-white">Attendance Pulse</div>
           <div class="flex flex-center">
              <q-knob
                readonly
                v-model="pulse"
                size="180px"
                :thickness="0.12"
                color="primary"
                track-color="surface-2"
                class="text-primary text-h4 text-heading"
                show-value
              >
                {{ pulse }}%
              </q-knob>
           </div>
           <div class="text-center q-mt-xl text-grey-5">Average across all groups</div>
        </q-card>
      </div>
    </div>

    <!-- Secondary Charts -->
    <div class="row q-col-gutter-lg q-mt-lg">
      <div class="col-12 col-md-6">
        <q-card flat bordered class="sams-card bg-surface-1 q-pa-xl" style="min-height: 350px">
           <div class="text-heading text-h6 q-mb-xl text-white">Enrollment Trends</div>
           <div v-if="enrollmentChartData" style="height: 280px">
              <Bar :data="enrollmentChartData" :options="chartOptions" />
           </div>
           <div v-else class="flex flex-center q-mt-xl opacity-20">
              <div class="text-h6 text-weight-light text-white">No enrollment data yet</div>
           </div>
        </q-card>
      </div>
      <div class="col-12 col-md-6">
        <q-card flat bordered class="sams-card bg-surface-1 q-pa-xl" style="min-height: 350px">
           <div class="text-heading text-h6 q-mb-xl text-white">Coach Performance</div>
           <div v-if="coachChartData" style="height: 280px">
              <Bar :data="coachChartData" :options="chartOptions" />
           </div>
           <div v-else class="flex flex-center q-mt-xl opacity-20">
              <div class="text-h6 text-weight-light text-white">No performance data yet</div>
           </div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line, Bar } from 'vue-chartjs';
import { useAnalyticsStore } from '../../stores/analytics';
import { useChart } from '../../composables/useChart';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const analyticsStore = useAnalyticsStore();
const { baseOptions } = useChart();

const pulse = ref(0);

const chartOptions = computed(() => baseOptions());

const revenueChartData = computed(() => {
  const data = analyticsStore.dailyRevenue;
  if (!data.length) return null;
  return {
    labels: data.map((d) => d.date),
    datasets: [
      {
        label: 'Revenue',
        data: data.map((d) => d.total),
        borderColor: '#3B82F6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.3,
      },
    ],
  };
});

const enrollmentChartData = computed(() => {
  const data = analyticsStore.monthlyEnrollment;
  if (!data.length) return null;
  return {
    labels: data.map((d) => d.month),
    datasets: [
      {
        label: 'New Enrollments',
        data: data.map((d) => d.new_enrollments),
        backgroundColor: '#22C55E',
      },
      {
        label: 'Cancelled',
        data: data.map((d) => d.cancelled),
        backgroundColor: '#EF4444',
      },
    ],
  };
});

const coachChartData = computed(() => {
  const data = analyticsStore.coachPerformance;
  if (!data.length) return null;
  return {
    labels: data.map((d) => d.coach_name),
    datasets: [
      {
        label: 'Avg Attendance %',
        data: data.map((d) => d.avg_attendance),
        backgroundColor: '#3B82F6',
      },
      {
        label: 'Avg Rating',
        data: data.map((d) => d.avg_rating),
        backgroundColor: '#F59E0B',
      },
    ],
  };
});

const analyticsStats = computed(() => {
  const revTotal = analyticsStore.dailyRevenue.reduce((s: number, d: any) => s + (d.total || 0), 0);
  const attData = analyticsStore.dailyAttendance;
  const avgAtt = attData.length
    ? Math.round(attData.reduce((s: number, d: any) => s + (d.attendance_rate || 0), 0) / attData.length)
    : 0;
  const enrollData = analyticsStore.monthlyEnrollment;
  const netEnroll = enrollData.length ? enrollData[enrollData.length - 1].net_change : 0;
  const coachData = analyticsStore.coachPerformance;
  const activeCoaches = coachData.filter((c: any) => c.sessions_held > 0).length;

  return [
    { label: 'Revenue (MTD)', value: `$${revTotal.toLocaleString()}`, positive: revTotal > 0, trend: revTotal > 0 ? 'Active' : 'None' },
    { label: 'Avg Attendance', value: `${avgAtt}%`, positive: avgAtt >= 70, trend: avgAtt >= 70 ? 'Healthy' : 'Low' },
    { label: 'Net Enrollment', value: String(netEnroll), positive: netEnroll >= 0, trend: netEnroll >= 0 ? 'Growing' : 'Shrinking' },
    { label: 'Active Coaches', value: String(activeCoaches), positive: activeCoaches > 0, trend: 'Engaged' },
  ];
});

onMounted(async () => {
  await Promise.all([
    analyticsStore.fetchRevenue(),
    analyticsStore.fetchAttendance(),
    analyticsStore.fetchEnrollment(),
    analyticsStore.fetchCoachPerformance(),
  ]);
  const attData = analyticsStore.dailyAttendance;
  if (attData.length) {
    pulse.value = Math.round(
      attData.reduce((s, d) => s + (d.attendance_rate || 0), 0) / attData.length
    );
  }
});
</script>

<style lang="scss" scoped>
.bg-surface-1 { background-color: var(--sams-surface-1); }
.bg-surface-2 { background-color: var(--sams-surface-2); }
.opacity-20 { opacity: 0.2; }
.letter-spacing-1 { letter-spacing: 1px; }
</style>
