<template>
  <q-page class="apex-auth flex flex-center">
    <div class="column items-center full-width animate-fade-in" style="max-width: 500px">
      <!-- Branded Header -->
      <div class="text-center q-mb-xl">
        <h2 class="text-apex text-navy no-margin">SAMS<span class="text-victory">.</span></h2>
        <div class="text-overline text-grey-6 letter-spacing-5">Athlete Enrollment</div>
      </div>

      <div class="login-container full-width">
        <div class="login-accent" style="background: var(--sams-victory-red)"></div>
        <div class="apex-card q-pa-xl">
          <div class="text-center q-mb-xl">
             <div class="text-h5 text-apex text-navy uppercase">Join the Academy</div>
             <div class="text-caption text-grey-6 q-mt-sm">Start your professional sports journey today</div>
          </div>

          <div class="row q-col-gutter-md">
            <div class="col-12 col-sm-6">
              <q-input v-model="regData.first_name" label="First Name" outlined stack-label color="navy" class="apex-input" />
            </div>
            <div class="col-12 col-sm-6">
              <q-input v-model="regData.last_name" label="Last Name" outlined stack-label color="navy" class="apex-input" />
            </div>
            <div class="col-12">
              <q-input v-model="regData.username" label="Username" outlined stack-label color="navy" class="apex-input" />
            </div>
            <div class="col-12">
              <q-input v-model="regData.email" label="Email Address" type="email" outlined stack-label color="navy" class="apex-input" />
            </div>
            <div class="col-12">
              <q-input v-model="regData.password" label="Password" type="password" outlined stack-label color="navy" class="apex-input" />
            </div>
          </div>

          <div class="q-mt-xl">
            <q-btn
              unelevated
              class="full-width q-py-md apex-btn-primary shadow-lg"
              label="Create Athlete Account"
              :loading="loading"
              @click="handleRegister"
            />
          </div>

          <div class="text-center q-mt-xl">
            <div class="text-grey-7 q-mb-sm">Already a member?</div>
            <q-btn flat color="navy" label="Sign In to Arena" :to="{ name: 'login-customer' }" dense no-caps class="text-weight-bold" />
          </div>
        </div>
      </div>

      <q-btn flat color="grey-7" label="Return to Home" to="/" icon="arrow_back" class="q-mt-lg" dense no-caps />
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
    router.push({ name: 'login-customer' });
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: error.response?.data?.detail || 'Registration failed. Please check your data.',
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
</style>
