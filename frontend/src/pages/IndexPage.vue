<template>
  <q-page class="landing-page flex flex-center overflow-hidden">
    <!-- Animated Background Elements -->
    <div class="bg-shape shape-1"></div>
    <div class="bg-shape shape-2"></div>
    <div class="bg-shape shape-3"></div>

    <div class="content-wrapper column items-center q-pa-lg">
      <!-- Hero Section -->
      <div class="hero-section text-center q-mb-xl">
        <div class="text-overline text-secondary text-weight-bolder letter-spacing-3 q-mb-sm">
          NEXT-GEN MANAGEMENT
        </div>
        <h1 class="text-h1 text-white text-weight-black no-margin sport-title">
          SAMS<span class="text-secondary">.</span>
        </h1>
        <div class="text-h6 text-grey-4 text-weight-light q-mt-md max-width-600">
          The heartbeat of Egyptian sports academies. Professional, modular, and built for champions.
        </div>
      </div>

      <!-- Portal Grid -->
      <div class="portal-grid row justify-center q-col-gutter-xl full-width max-width-1000">
        <!-- Customer Portal Card -->
        <div class="col-12 col-sm-4">
          <q-card class="portal-card glass-card text-white cursor-pointer" @click="$router.push({ name: 'login' })">
            <q-card-section class="column items-center q-py-xl">
              <div class="icon-box q-mb-lg">
                <q-icon name="group" size="48px" color="secondary" />
              </div>
              <div class="text-h5 text-weight-bold q-mb-sm">CUSTOMERS</div>
              <div class="text-caption text-grey-4 text-center">Manage your children's training, ratings, and schedule.</div>
              <q-btn flat color="secondary" label="Enter Arena" icon-right="chevron_right" class="q-mt-md" />
            </q-card-section>
          </q-card>
        </div>

        <!-- Coach Portal Card -->
        <div class="col-12 col-sm-4">
          <q-card class="portal-card glass-card text-white cursor-pointer" @click="$router.push({ name: 'login' })">
            <q-card-section class="column items-center q-py-xl">
              <div class="icon-box q-mb-lg">
                <q-icon name="sports" size="48px" color="accent" />
              </div>
              <div class="text-h5 text-weight-bold q-mb-sm">COACHES</div>
              <div class="text-caption text-grey-4 text-center">Track attendance, submit reports, and rate performance.</div>
              <q-btn flat color="accent" label="Start Session" icon-right="chevron_right" class="q-mt-md" />
            </q-card-section>
          </q-card>
        </div>

        <!-- Operations Portal Card -->
        <div class="col-12 col-sm-4">
          <q-card class="portal-card glass-card text-white cursor-pointer" @click="$router.push({ name: 'login' })">
            <q-card-section class="column items-center q-py-xl">
              <div class="icon-box q-mb-lg">
                <q-icon name="admin_panel_settings" size="48px" color="info" />
              </div>
              <div class="text-h5 text-weight-bold q-mb-sm">OPERATIONS</div>
              <div class="text-caption text-grey-4 text-center">Manage players, finances, and academy settings.</div>
              <q-btn flat color="info" label="HQ Command" icon-right="chevron_right" class="q-mt-md" />
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Footer Action -->
      <div class="q-mt-xl text-center">
        <q-btn
          flat
          rounded
          color="grey-5"
          label="Academy Staff Login"
          icon="admin_panel_settings"
          class="staff-btn"
          :to="{ name: 'login' }"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
// Creative Landing Page Implementation
</script>

<style lang="scss" scoped>
.landing-page {
  background: linear-gradient(135deg, #0d123d 0%, #1a237e 100%);
  min-height: 100vh;
  position: relative;
  font-family: 'Inter', sans-serif;
}

.sport-title {
  font-size: clamp(5rem, 15vw, 10rem);
  line-height: 1;
  letter-spacing: -4px;
}

.letter-spacing-3 {
  letter-spacing: 4px;
}

.max-width-600 { max-width: 600px; }
.max-width-1000 { max-width: 1000px; }

// Animated Shapes
.bg-shape {
  position: absolute;
  filter: blur(80px);
  z-index: 0;
  opacity: 0.4;
  border-radius: 50%;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: $secondary;
  top: -100px;
  left: -100px;
  animation: float 20s infinite alternate;
}

.shape-2 {
  width: 500px;
  height: 500px;
  background: $accent;
  bottom: -150px;
  right: -100px;
  animation: float 25s infinite alternate-reverse;
}

.shape-3 {
  width: 300px;
  height: 300px;
  background: #6200ea;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.2;
}

@keyframes float {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(100px, 50px) scale(1.1); }
}

.content-wrapper {
  position: relative;
  z-index: 1;
}

.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);

  &:hover {
    transform: translateY(-15px) scale(1.02);
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    
    .icon-box {
      transform: scale(1.1) rotate(5deg);
    }
  }
}

.icon-box {
  background: rgba(255, 255, 255, 0.05);
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 30px;
  transition: transform 0.3s ease;
}

.staff-btn {
  font-size: 14px;
  text-transform: none;
  opacity: 0.7;
  &:hover { opacity: 1; }
}
</style>
