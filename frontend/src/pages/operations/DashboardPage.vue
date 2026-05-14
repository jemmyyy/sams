<template>
  <q-page class="q-pa-lg">
    <div class="text-h4 text-weight-bold q-mb-xl text-dark">HQ <span class="text-info">Overview</span></div>
    
    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-4">
        <q-card flat bordered class="ops-card">
          <q-card-section>
            <div class="text-subtitle1 text-grey-6 uppercase">Total Players</div>
            <div class="text-h3 text-weight-black">245</div>
            <div class="text-caption text-positive"><q-icon name="trending_up" /> 12% this month</div>
          </q-card-section>
        </q-card>
      </div>
      
      <div class="col-12 col-md-4">
        <q-card flat bordered class="ops-card">
          <q-card-section>
            <div class="text-subtitle1 text-grey-6 uppercase">Active Sessions</div>
            <div class="text-h3 text-weight-black">18</div>
            <div class="text-caption text-grey-6">Across 3 Venues</div>
          </q-card-section>
        </q-card>
      </div>
      
      <div class="col-12 col-md-4">
        <q-card flat bordered class="ops-card">
          <q-card-section>
            <div class="text-subtitle1 text-grey-6 uppercase">Pending Cancellations</div>
            <div class="text-h3 text-weight-black text-warning">5</div>
            <div class="text-caption text-grey-6">Require review</div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<style scoped>
.ops-card {
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}
</style>
