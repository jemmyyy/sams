<template>
  <q-page class="sams-landing full-viewport flex flex-center">
    <!-- Hero Background (Subtle Gradient) -->
    <div class="landing-bg"></div>

    <div class="max-w-xl full-width q-pa-xl column items-center text-center animate-up">
      <!-- High-Impact Brand Header -->
      <div class="hero-content q-mb-xl">
        <div class="row items-center justify-center q-mb-sm">
           <q-badge rounded color="primary" class="q-mr-sm" />
           <span class="text-overline text-primary text-weight-bold letter-spacing-5">Premium Sports Intelligence</span>
        </div>
        <h1 class="text-heading heading-xl no-margin">SAMS<span class="text-primary">.</span></h1>
        <p class="text-h6 text-grey-7 text-weight-light max-width-600 q-mx-auto q-mt-md">
          Empowering the next generation of Egyptian champions. One integrated platform for <span class="text-weight-bold text-white">Logistics, Performance, and Growth.</span>
        </p>
      </div>

      <!-- Clean Portal Selection -->
      <div class="row q-col-gutter-lg justify-center full-width items-stretch">
        <!-- Customer Portal -->
        <div class="col-12 col-md-4">
          <q-card flat bordered class="sams-card portal-choice q-pa-xl column full-height">
            <q-card-section class="column items-center">
              <q-icon name="group" size="56px" color="primary" class="q-mb-md" />
              <div class="text-heading text-h5 text-white">Athlete Arena</div>
              <div class="text-caption text-grey-6 q-mt-sm">Parents & Players Portal</div>
            </q-card-section>
            <q-space />
            <q-card-actions vertical class="q-gutter-y-sm q-pa-none q-mt-lg">
              <q-btn unelevated color="primary" :label="$t('auth.signIn')" @click="goToLogin('customer')" class="full-width sams-btn" />
              <q-btn outline color="primary" :label="$t('auth.joinAcademy')" to="/auth/register" class="full-width sams-btn" />
            </q-card-actions>
          </q-card>
        </div>

        <!-- Coach Portal -->
        <div class="col-12 col-md-4">
          <q-card flat bordered class="sams-card portal-choice q-pa-xl column full-height featured">
            <q-card-section class="column items-center">
              <q-icon name="sports" size="56px" color="white" class="q-mb-md" />
              <div class="text-heading text-h5 text-white">Tactical Field</div>
              <div class="text-caption text-grey-4 q-mt-sm">Coach Command Center</div>
            </q-card-section>
            <q-space />
            <q-card-actions vertical class="q-gutter-y-sm q-pa-none q-mt-lg">
              <q-btn unelevated color="primary" :label="$t('auth.signIn')" @click="goToLogin('coach')" class="full-width sams-btn" />
              <div style="height: 36px"></div> <!-- Spacer to match Join Academy button height -->
            </q-card-actions>
          </q-card>
        </div>

        <!-- Operations Portal -->
        <div class="col-12 col-md-4">
          <q-card flat bordered class="sams-card portal-choice q-pa-xl column full-height">
            <q-card-section class="column items-center">
              <q-icon name="admin_panel_settings" size="56px" color="primary" class="q-mb-md" />
              <div class="text-heading text-h5">Academy HQ</div>
              <div class="text-caption text-grey-6 q-mt-sm">Operational Command</div>
            </q-card-section>
            <q-space />
            <q-card-actions vertical class="q-gutter-y-sm q-pa-none q-mt-lg">
              <q-btn unelevated color="primary" :label="$t('auth.signIn')" @click="goToLogin('operations')" class="full-width sams-btn" />
              <div style="height: 36px"></div> <!-- Spacer to match Join Academy button height -->
            </q-card-actions>
          </q-card>
        </div>
      </div>

      <!-- Language Toggle -->
      <div class="q-mt-xl">
        <q-btn 
          flat 
          color="grey-5" 
          :label="appStore.locale === 'en-US' ? 'العربية' : 'English'" 
          icon="language" 
          @click="appStore.toggleLocale" 
          class="text-weight-bold"
        />
      </div>

      <!-- Grounded Footer -->
      <div class="q-mt-lg row items-center q-gutter-md text-grey-6">
        <span class="text-mono text-min uppercase">©2026 SAMS Architecture</span>
        <q-separator vertical inset dark class="opacity-20" />
        <span class="text-mono text-min uppercase">Secure Enterprise Environment</span>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useAppStore } from '../stores/app';

const router = useRouter();
const appStore = useAppStore();

function goToLogin(role: string) {
  router.push({ name: 'login', query: { role } });
}
</script>

<style lang="scss" scoped>
.sams-landing {
  background-color: var(--sams-bg);
  position: relative;
  overflow: hidden;
}

.landing-bg {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: radial-gradient(circle at 70% 20%, rgba(37, 99, 235, 0.05) 0%, transparent 50%),
              radial-gradient(circle at 10% 80%, rgba(37, 99, 235, 0.03) 0%, transparent 40%);
  z-index: 0;
}

.max-width-600 { max-width: 600px; }
.letter-spacing-5 { letter-spacing: 5px; }

.portal-choice {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border-width: 2px;
  
  &:hover {
    border-color: var(--sams-primary);
    transform: translateY(-10px);
  }

  &.featured {
    background: var(--sams-navy);
    border: none;
    box-shadow: 0 20px 40px -8px rgba(15, 23, 42, 0.3);
    
    &:hover {
      background: #1e293b;
      box-shadow: 0 30px 60px -12px rgba(15, 23, 42, 0.4);
    }
  }
}

.text-min { font-size: 11px; }
</style>
