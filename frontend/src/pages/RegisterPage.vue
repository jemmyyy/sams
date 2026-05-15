<template>
  <q-page class="sams-auth-dark flex flex-center">
    <div class="column items-center full-width animate-up" style="max-width: 500px">
      <!-- Branded Header -->
      <div class="text-center q-mb-xl">
        <h2 class="text-heading text-white no-margin">SAMS<span class="text-primary">.</span></h2>
        <div class="text-overline text-grey-6 letter-spacing-5">Athlete Enrollment</div>
      </div>

      <q-card flat bordered class="sams-card full-width q-pa-xl">
        <div class="text-center q-mb-xl">
           <div class="text-h5 text-heading text-white uppercase">Join the Academy</div>
           <div class="text-caption text-grey-6 q-mt-sm">Start your professional sports journey today</div>
        </div>

        <div class="row q-col-gutter-md">
          <div class="col-12 col-sm-6">
            <q-input v-model="regData.first_name" label="First Name" outlined dark stack-label color="primary" class="sams-input-dark" />
          </div>
          <div class="col-12 col-sm-6">
            <q-input v-model="regData.last_name" label="Last Name" outlined dark stack-label color="primary" class="sams-input-dark" />
          </div>
          <div class="col-12">
            <q-input v-model="regData.username" label="Username" outlined dark stack-label color="primary" class="sams-input-dark" />
          </div>
          <div class="col-12">
            <q-input v-model="regData.email" label="Email Address" type="email" outlined dark stack-label color="primary" class="sams-input-dark" />
          </div>
          <div class="col-12">
            <q-input v-model="regData.password" label="Password" type="password" outlined dark stack-label color="primary" class="sams-input-dark" />
          </div>
        </div>

        <div class="q-mt-xl">
          <q-btn
            unelevated
            class="full-width q-py-md sams-btn-action-dark"
            label="Create Athlete Account"
            :loading="loading"
            @click="handleRegister"
          />
        </div>

        <div class="text-center q-mt-xl">
          <div class="text-grey-7 q-mb-sm">Already a member?</div>
          <q-btn flat color="primary" label="Sign In to Arena" :to="{ name: 'login-customer' }" dense no-caps class="text-weight-bold" />
        </div>
      </q-card>

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
</style>
