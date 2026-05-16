<template>
  <q-page class="sams-auth-dark flex flex-center">
    <div class="column items-center full-width animate-up" style="max-width: 420px">
      <!-- Branded Header -->
      <div class="text-center q-mb-xl">
        <h2 class="text-heading text-white no-margin">SAMS<span class="text-primary">.</span></h2>
        <div class="text-overline text-grey-6 letter-spacing-5">Secure Access Gateway</div>
      </div>

      <!-- Professional Login Card -->
      <q-card flat bordered class="sams-card full-width q-pa-xl">
        <div class="text-center q-mb-xl">
           <div class="text-h5 text-heading text-white uppercase">{{ targetRole }} {{ $t('auth.signIn') }}</div>
           <div class="text-caption text-grey-6 q-mt-sm">Access your academy dashboard</div>
        </div>

        <div class="q-gutter-y-lg">
          <SamsInput
            v-model="loginData.username"
            :label="$t('auth.username')"
          >
            <template v-slot:prepend>
              <q-icon name="person_outline" color="grey-6" />
            </template>
          </SamsInput>

          <SamsInput
            v-model="loginData.password"
            :label="$t('auth.password')"
            type="password"
            @keyup.enter="handleLogin"
          >
            <template v-slot:prepend>
              <q-icon name="lock_outline" color="grey-6" />
            </template>
          </SamsInput>
        </div>

        <div class="text-right q-mb-sm">
          <q-btn flat dense color="grey-5" label="Forgot password?" no-caps class="text-caption" to="/auth/forgot-password" />
        </div>

        <div class="q-mt-sm">
          <q-btn
            unelevated
            class="full-width q-py-md sams-btn-primary"
            :label="$t('auth.signIn')"
            :loading="loading"
            @click="handleLogin"
          />
        </div>

        <div class="text-center q-mt-xl">
          <template v-if="targetRole === 'customer'">
            <div class="text-grey-7 q-mb-sm">Don't have an athlete account?</div>
            <q-btn flat color="primary" :label="$t('auth.register')" to="/auth/register" class="text-weight-bold q-mb-md" no-caps />
          </template>
          <div>
            <q-btn flat color="grey-7" :label="$t('common.backToHome')" to="/" icon="arrow_back" dense no-caps />
          </div>
        </div>
      </q-card>

      <!-- Language Toggle in Auth -->
      <q-btn 
        flat 
        color="grey-6" 
        size="sm"
        :label="appStore.locale === 'en-US' ? 'العربية' : 'English'" 
        @click="appStore.toggleLocale" 
        class="q-mt-lg"
      />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useAppStore } from '../stores/app';
import { useQuasar } from 'quasar';
import SamsInput from '../components/common/SamsInput.vue';

const $q = useQuasar();
const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const appStore = useAppStore();

const loading = ref(false);
const loginData = reactive({
  username: '',
  password: ''
});

const targetRole = computed(() => {
  if (route.meta.targetRole) return route.meta.targetRole as string;
  return (route.query.role as string) || 'customer';
});

async function handleLogin() {
  if (!loginData.username || !loginData.password) return;
  
  loading.value = true;
  try {
    await authStore.login(loginData);
    
    if (!authStore.hasRole(targetRole.value)) {
      $q.notify({
        message: 'Unauthorized: Invalid role for this portal.',
        color: 'negative',
        icon: 'security',
        position: 'top'
      });
      authStore.logout();
      return;
    }

    $q.notify({
      message: 'Login Successful',
      color: 'positive',
      icon: 'check',
      position: 'top'
    });

    const redirectPath = route.query.redirect as string;
    if (redirectPath) {
      router.push(redirectPath);
    } else {
      router.push({ name: authStore.primaryPortal });
    }

  } catch (error: any) {
    let msg = 'Authentication failed.';
    if (!error.response) {
      msg = 'Network error. Cannot reach the server.';
    } else if (error.response.data?.detail) {
      msg = error.response.data.detail;
    } else if (error.response.data?.non_field_errors) {
      msg = error.response.data.non_field_errors[0];
    }
    
    $q.notify({
      message: msg,
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
.sams-auth-dark {
  background-color: var(--sams-bg);
  min-height: 100vh;
}

.sams-input-dark {
  :deep(.q-field__control) {
    background-color: var(--sams-surface-1);
    border-radius: 12px;
  }
}

.sams-btn-action-dark {
  background: var(--sams-primary);
  color: white;
  border-radius: 10px;
  font-weight: 700;
  &:hover { background: #1d4ed8; }
}

.letter-spacing-5 { letter-spacing: 5px; }
.opacity-40 { opacity: 0.4; }
</style>
