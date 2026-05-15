<template>
  <q-page class="apex-landing flex flex-center no-scroll">
    <!-- Subtle Background Accent -->
    <div class="bg-accent-blob"></div>

    <div class="content-container column items-center full-width animate-fade-in">
      <!-- High-Impact Hero -->
      <div class="hero-section text-center q-mb-xl">
        <div class="row items-center justify-center q-mb-sm">
           <div class="victory-line"></div>
           <span class="text-apex text-victory uppercase letter-spacing-5 q-mx-md">Elite Performance</span>
           <div class="victory-line"></div>
        </div>
        <h1 class="heading-xl text-apex text-navy no-margin">SAMS<span class="text-victory">.</span></h1>
        <p class="text-h6 text-grey-7 text-weight-light max-width-600 q-mt-md">
          The premium intelligence layer for Egypt's leading sports academies. 
          <span class="text-weight-bold text-navy">Built for champions, by experts.</span>
        </p>
      </div>

      <!-- Balanced Portal Grid -->
      <div class="portal-grid row justify-center q-col-gutter-xl full-width max-w-xl">
        <!-- CUSTOMER PORTAL -->
        <div class="col-12 col-md-4">
          <div class="apex-portal-card column items-center q-pa-xl cursor-pointer" @click="$router.push({ name: 'login-customer' })">
            <div class="portal-icon-container bg-slate row justify-center items-center q-mb-lg">
               <q-icon name="groups" size="48px" color="navy" />
            </div>
            <div class="text-apex text-h5 text-navy q-mb-sm">ARENA</div>
            <div class="text-caption text-grey-6 text-center uppercase letter-spacing-1">Athlete & Parent Access</div>
            <q-btn flat class="q-mt-xl text-weight-bold text-navy" label="Enter Arena" icon-right="arrow_forward" />
          </div>
        </div>

        <!-- COACH PORTAL -->
        <div class="col-12 col-md-4">
          <div class="apex-portal-card column items-center q-pa-xl cursor-pointer featured-card" @click="$router.push({ name: 'login-coach' })">
            <div class="portal-icon-container bg-victory row justify-center items-center q-mb-lg">
               <q-icon name="sports" size="48px" color="white" />
            </div>
            <div class="text-apex text-h5 text-white q-mb-sm">FIELD</div>
            <div class="text-caption text-white opacity-80 text-center uppercase letter-spacing-1">Tactical Coach Command</div>
            <q-btn flat class="q-mt-xl text-weight-bold text-white" label="Deploy to Field" icon-right="bolt" />
          </div>
        </div>

        <!-- OPERATIONS PORTAL -->
        <div class="col-12 col-md-4">
          <div class="apex-portal-card column items-center q-pa-xl cursor-pointer" @click="$router.push({ name: 'login-ops' })">
            <div class="portal-icon-container bg-slate row justify-center items-center q-mb-lg">
               <q-icon name="dashboard_customize" size="48px" color="navy" />
            </div>
            <div class="text-apex text-h5 text-navy q-mb-sm">HQ</div>
            <div class="text-caption text-grey-6 text-center uppercase letter-spacing-1">Academy Logistics HQ</div>
            <q-btn flat class="q-mt-xl text-weight-bold text-navy" label="HQ Command" icon-right="shield" />
          </div>
        </div>
      </div>

      <!-- Clean Footer Tech -->
      <div class="landing-footer full-width row items-center justify-between q-px-xl q-py-lg">
        <div class="row items-center q-gutter-md">
           <q-badge rounded color="green" class="status-dot" />
           <span class="text-mono text-caption text-grey-6">SYSTEM STATUS: OPTIMAL</span>
        </div>
        <div class="text-mono text-caption text-grey-6">©2026 SAMS ARCHITECTURE // VERSION 1.2</div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
const router = useRouter();

function goToLogin(role: string) {
  router.push({ name: 'login', query: { role } });
}
</script>

<style lang="scss" scoped>
.apex-landing {
  background-color: var(--sams-slate-bg);
  position: relative;
  overflow: hidden;
}

.bg-accent-blob {
  position: absolute;
  top: -10%; right: -5%;
  width: 40vw; height: 40vw;
  background: radial-gradient(circle, rgba(225, 29, 72, 0.05) 0%, transparent 70%);
  z-index: 0;
}

.text-navy { color: var(--sams-navy); }
.text-victory { color: var(--sams-victory-red); }
.letter-spacing-5 { letter-spacing: 5px; }

.victory-line { width: 40px; height: 2px; background: var(--sams-victory-red); }

.apex-portal-card {
  background: white;
  border-radius: 24px;
  border: 1px solid var(--sams-border);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 1;
  
  &:hover {
    transform: translateY(-12px);
    box-shadow: 0 30px 60px -12px rgba(15, 23, 42, 0.12);
    border-color: rgba(15, 23, 42, 0.1);
  }
}

.featured-card {
  background: var(--sams-navy);
  box-shadow: 0 20px 40px -8px rgba(15, 23, 42, 0.3);
  border: none;
  &:hover {
    box-shadow: 0 30px 60px -12px rgba(225, 29, 72, 0.3);
    background: #0f172a;
  }
}

.portal-icon-container {
  width: 90px; height: 90px;
  border-radius: 20px;
  &.bg-slate { background: #f1f5f9; }
  &.bg-victory { background: var(--sams-victory-red); }
}

.landing-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  border-top: 1px solid var(--sams-border);
}

.status-dot { width: 8px; height: 8px; }
.max-width-600 { max-width: 600px; }
</style>
