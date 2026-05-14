<template>
  <q-page class="auth-bg flex flex-center q-pa-md">
    <div class="column items-center full-width" style="max-width: 450px">
      <!-- Logo/Brand -->
      <div class="text-center q-mb-xl">
        <h1 class="text-h2 text-white text-weight-black no-margin">SAMS<span class="text-secondary">.</span></h1>
        <div class="text-overline text-grey-4 letter-spacing-3">ATHLETE COMMAND</div>
      </div>

      <q-card class="auth-card glass-card full-width q-pa-lg shadow-24 text-white">
        <q-card-section class="text-center q-pb-none">
          <div class="text-h5 text-weight-bold uppercase letter-spacing-1">SIGN IN</div>
          <div class="text-body2 text-grey-4 q-mt-sm">Access your training dashboard</div>
        </q-card-section>

        <q-card-section class="q-gutter-y-lg q-mt-md">
          <q-input
            v-model="loginData.username"
            label="Username"
            filled
            dark
            color="secondary"
            class="sport-input"
            :rules="[val => !!val || 'Field is required']"
          >
            <template v-slot:prepend>
              <q-icon name="person" />
            </template>
          </q-input>

          <q-input
            v-model="loginData.password"
            label="Password"
            type="password"
            filled
            dark
            color="secondary"
            class="sport-input"
            @keyup.enter="handleLogin"
            :rules="[val => !!val || 'Field is required']"
          >
            <template v-slot:prepend>
              <q-icon name="lock" />
            </template>
          </q-input>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-btn
            color="secondary"
            class="full-width q-py-md text-weight-black"
            size="lg"
            label="LOGIN TO ARENA"
            :loading="loading"
            @click="handleLogin"
          />
        </q-card-section>

        <q-card-section class="text-center text-grey-4">
          Don't have an account? 
          <q-btn flat color="secondary" label="Register Now" to="/register" dense no-caps class="text-weight-bold" />
        </q-card-section>
      </q-card>

      <q-btn flat color="grey-5" label="Back to Home" icon="arrow_back" to="/" class="q-mt-lg" />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from 'stores/auth';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const router = useRouter();
const authStore = useAuthStore();

const loading = ref(false);
const loginData = reactive({
  username: '',
  password: ''
});

async function handleLogin() {
  if (!loginData.username || !loginData.password) return;
  
  loading.ref = true;
  try {
    await authStore.login(loginData);
    $q.notify({
      type: 'positive',
      message: 'Login Successful! Welcome back champion.',
      position: 'top'
    });
    
    // In a real app, logic would check role to redirect. 
    // For now, we'll default to customer as a placeholder.
    router.push('/customer/timetable');
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: error.response?.data?.detail || 'Authentication failed. Please check your credentials.',
      position: 'top'
    });
  } finally {
    loading.value = false;
  }
}
</script>

<style lang="scss" scoped>
.auth-card {
  border-radius: 32px;
}

.letter-spacing-3 { letter-spacing: 3px; }
.letter-spacing-1 { letter-spacing: 1px; }

.sport-input {
  :deep(.q-field__control) {
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.05);
  }
}

.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
