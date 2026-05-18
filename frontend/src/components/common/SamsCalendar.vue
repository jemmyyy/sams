<template>
  <div class="sams-calendar">
    <div class="row items-center justify-between q-mb-md">
      <div class="row items-center q-gutter-sm">
        <q-btn flat round icon="chevron_left" @click="prevMonth" color="grey-5" size="sm" aria-label="Previous month" />
        <span class="text-h6 text-white text-weight-medium">{{ monthLabel }}</span>
        <q-btn flat round icon="chevron_right" @click="nextMonth" color="grey-5" size="sm" aria-label="Next month" />
      </div>
      <q-btn flat round icon="today" @click="goToday" color="primary" size="sm" aria-label="Go to today">
        <q-tooltip>Today</q-tooltip>
      </q-btn>
    </div>

    <div class="calendar-grid">
      <div v-for="day in weekDays" :key="day" class="calendar-header text-grey-5 text-weight-bold text-caption">
        {{ day }}
      </div>
      <div
        v-for="(day, i) in monthDays"
        :key="i"
        class="calendar-cell"
        :class="{
          'calendar-cell--today': day.isToday,
          'calendar-cell--outside': !day.isCurrentMonth,
        }"
      >
        <span class="calendar-day-number">{{ day.dayNumber }}</span>
        <div class="calendar-events">
          <div
            v-for="event in getEvents(day.iso)"
            :key="event.id"
            class="calendar-event"
            :style="{ background: event.color || 'var(--sams-primary)' }"
          >
            {{ event.title }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useCalendar } from '../../composables/useCalendar'
import type { CalendarDay } from '../../composables/useCalendar'

const props = defineProps<{
  events?: { id: string; date: string; title: string; color?: string }[]
}>()

const { monthDays, weekDays, prevMonth, nextMonth, goToday, monthLabel } = useCalendar()

function getEvents(iso: string) {
  return (props.events || []).filter((e) => e.date === iso).slice(0, 3)
}
</script>

<style lang="scss" scoped>
.sams-calendar {
  user-select: none;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background: var(--sams-border);
  border: 1px solid var(--sams-border);
  border-radius: 8px;
  overflow: hidden;
}

.calendar-header {
  padding: 8px 4px;
  text-align: center;
  background: var(--sams-surface-2);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.calendar-cell {
  min-height: 80px;
  padding: 4px;
  background: var(--sams-surface-1);
}

.calendar-cell--outside {
  opacity: 0.35;
}

.calendar-cell--today {
  .calendar-day-number {
    background: var(--sams-primary);
    color: white;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
  }
}

.calendar-day-number {
  font-size: 12px;
  color: var(--sams-text-secondary);
  margin-bottom: 2px;
}

.calendar-events {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.calendar-event {
  font-size: 10px;
  padding: 1px 4px;
  border-radius: 3px;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
