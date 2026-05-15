<template>
  <q-page class="apex-auth flex flex-center">
    <div class="column items-center full-width animate-fade-in" style="max-width: 440px">
      <!-- Branded Header -->
      <div class="text-center q-mb-xl">
        <h2 class="text-apex text-navy no-margin">SAMS<span class="text-victory">.</span></h2>
        <div class="text-overline text-grey-6 letter-spacing-5">Apex Performance Layer</div>
      </div>

      <!-- Professional Login Card -->
      <div class="login-container full-width">
        <div class="login-accent" :style="{ background: roleColor }"></div>
        <div class="apex-card q-pa-xl">
          <div class="text-center q-mb-xl">
             <div class="text-h5 text-apex text-navy uppercase">{{ targetRole }} Sign In</div>
             <div class="text-caption text-grey-6 q-mt-sm">Enter your authorized credentials below</div>
          </div>

          <div class="q-gutter-y-lg">
            <q-input
              v-model="loginData.username"
              label="Username"
              outlined
              stack-label
              color="navy"
              class="apex-input"
            >
              <template v-slot:prepend>
                <q-icon name="person_outline" color="grey-6" />
              </template>
            </q-input>

            <q-input
              v-model="loginData.password"
              label="Secure Passkey"
              type="password"
              outlined
              stack-label
              color="navy"
              class="apex-input"
              @keyup.enter="handleLogin"
            >
              <template v-slot:prepend>
                <q-icon name="lock_open" color="grey-6" />
              </template>
            </q-input>
          </div>

          <div class="q-mt-xl">
            <q-btn
              unelevated
              class="full-width q-py-md apex-btn-primary shadow-lg"
              label="Initialize Access"
              :loading="loading"
              @click="handleLogin"
            />
          </div>

          <div class="text-center q-mt-xl">
            <q-btn flat color="grey-7" label="Return to Portal Gateway" to="/" icon="arrow_back" dense no-caps />
          </div>
        </div>
      </div>

      <!-- Security Trust Footer -->
      <div class="row items-center q-mt-xl q-gutter-md opacity-40">
         <q-icon name="verified_user" size="20px" />
         <span class="text-mono text-caption uppercase">End-to-End Encryption Active</span>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const loading = ref(false);
const loginData = reactive({
  username: '',
  password: ''
});

const targetRole = computed(() => {
  if (route.meta.targetRole) return route.meta.targetRole as string;
  return (route.query.role as string) || 'customer';
});

const roleColor = computed(() => {
  switch (targetRole.value) {
    case 'coach': return 'var(--sams-victory-red)';
    case 'operations': return 'var(--sams-navy)';
    default: return '#3b82f6'; // Professional blue for customers
  }
});

async function handleLogin() {
  if (!loginData.username || !loginData.password) return;
  
  loading.value = true;
  try {
    await authStore.login(loginData);
    
    // Check if user has the required role
    const hasAccess = authStore.hasRole(targetRole.value);

    if (!hasAccess) {
      $q.notify({
        message: `UNAUTHORIZED: This account lacks clearance for ${targetRole.value.toUpperCase()} access.`,
        color: 'negative',
        icon: 'security',
        position: 'top'
      });
      authStore.logout();
      return;
    }

    $q.notify({
      message: 'AUTHENTICATED: Session initialized.',
      color: 'positive',
      icon: 'done_all',
      position: 'top'
    });

    // CRITICAL: Redirection Logic
    const redirectPath = route.query.redirect as string;
    if (redirectPath) {
      router.push(redirectPath);
    } else {
      const targetPortal = authStore.primaryPortal;
      router.push({ name: targetPortal });
    }

  } catch (error: any) {
    $q.notify({
      message: error.response?.data?.detail || 'INVALID_CREDENTIALS: Check and retry.',
      color: 'negative',
      icon: 'error_outline',
      position: 'top'
    });
  } finally {
    loading.value = false;
  }
}
</script>

<style lang="scss" scoped>
.apex-auth {
  background-color: var(--sams-slate-bg);
  min-height: 100vh;
}

.text-navy { color: var(--sams-navy); }
.text-victory { color: var(--sams-victory-red); }
.letter-spacing-5 { letter-spacing: 5px; }

.login-container {
  position: relative;
}

.login-accent {
  position: absolute;
  top: -2px; left: 50%; transform: translateX(-50%);
  width: 100px; height: 4px;
  border-radius: 0 0 4px 4px;
  z-index: 2;
}

.apex-card {
  border-radius: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.08);
}

.apex-input {
  :deep(.q-field__control) {
    border-radius: 12px;
    background: #f8fafc;
    &:hover { background: #f1f5f9; }
  }
}

.opacity-40 { opacity: 0.4; }
</style>
