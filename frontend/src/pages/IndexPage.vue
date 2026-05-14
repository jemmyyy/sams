<template>
  <q-page class="flex flex-center bg-grey-1">
    <div class="column items-center q-gutter-y-xl" style="width: 100%; max-width: 400px">
      <div class="text-center">
        <div class="text-h3 text-primary text-weight-bold">SAMS</div>
        <div class="text-subtitle1 text-grey-7">Sports Academy Management System</div>
      </div>

      <q-card flat bordered class="full-width q-pa-lg shadow-2 bg-white">
        <q-card-section class="text-center">
          <div class="text-h5 q-mb-md">Welcome</div>
          <div class="text-body2 text-grey-6 q-mb-lg">Please select your portal to continue</div>
        </q-card-section>

        <q-card-section class="q-gutter-y-md">
          <q-btn
            color="primary"
            class="full-width"
            size="lg"
            label="Customer Portal"
            icon="person"
            to="/customer/timetable"
            outline
          />
          <q-btn
            color="secondary"
            class="full-width"
            size="lg"
            label="Coach Portal"
            icon="sports"
            to="/coach/timetable"
            outline
          />
        </q-card-section>

        <q-card-section class="text-center q-pt-lg">
          <q-btn flat color="grey-6" label="Staff Login" icon="admin_panel_settings" dense />
        </q-card-section>
      </q-card>

      <div class="text-caption text-grey-5">
        &copy; 2026 SAMS Egypt. All rights reserved.
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
// Landing page for SAMS
</script>

<style scoped>
.q-card {
  border-radius: 16px;
}
</style>
