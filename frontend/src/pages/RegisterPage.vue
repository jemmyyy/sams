<template>
  <q-page class="auth-bg flex flex-center q-pa-md">
    <div class="column items-center full-width" style="max-width: 500px">
      <!-- Logo/Brand -->
      <div class="text-center q-mb-lg">
        <h1 class="text-h3 text-white text-weight-black no-margin">SAMS<span class="text-secondary">.</span></h1>
        <div class="text-overline text-grey-4 letter-spacing-3">NEW ATHLETE REGISTRATION</div>
      </div>

      <q-card class="auth-card glass-card full-width q-pa-lg shadow-24 text-white">
        <q-card-section class="text-center q-pb-none">
          <div class="text-h5 text-weight-bold uppercase letter-spacing-1">CREATE ACCOUNT</div>
          <div class="text-body2 text-grey-4 q-mt-sm">Join the championship management system</div>
        </q-card-section>

        <q-card-section class="row q-col-gutter-md q-mt-md">
          <div class="col-12 col-sm-6">
            <q-input v-model="regData.first_name" label="First Name" filled dark color="secondary" class="sport-input" />
          </div>
          <div class="col-12 col-sm-6">
            <q-input v-model="regData.last_name" label="Last Name" filled dark color="secondary" class="sport-input" />
          </div>
          <div class="col-12">
            <q-input v-model="regData.username" label="Username" filled dark color="secondary" class="sport-input" />
          </div>
          <div class="col-12">
            <q-input v-model="regData.email" label="Email Address" type="email" filled dark color="secondary" class="sport-input" />
          </div>
          <div class="col-12">
            <q-input v-model="regData.password" label="Password" type="password" filled dark color="secondary" class="sport-input" />
          </div>
        </q-card-section>

        <q-card-section>
          <q-btn
            color="secondary"
            class="full-width q-py-md text-weight-black"
            size="lg"
            label="START MY JOURNEY"
            :loading="loading"
            @click="handleRegister"
          />
        </q-card-section>

        <q-card-section class="text-center text-grey-4">
          Already have an account? 
          <q-btn flat color="secondary" label="Sign In" to="/auth/login" dense no-caps class="text-weight-bold" />
        </q-card-section>
      </q-card>
      
      <q-btn flat color="grey-5" label="Back to Home" icon="arrow_back" to="/" class="q-mt-lg" />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const router = useRouter();

const loading = ref(false);
const regData = reactive({
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  password: ''
});

async function handleRegister() {
  loading.value = true;
  try {
    await api.post('accounts/register/', regData);
    $q.notify({
      type: 'positive',
      message: 'Account created! Please sign in.',
      position: 'top'
    });
    router.push('/auth/login');
  } catch (error: unknown) {
    const err = error as { response?: { data?: { detail?: string } } };
    $q.notify({
      type: 'negative',
      message: err.response?.data?.detail || 'Registration failed. Please check your data.',
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
