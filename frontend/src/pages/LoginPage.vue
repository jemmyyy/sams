<template>
  <q-page class="sams-auth flex flex-center">
    <div class="column items-center full-width animate-up" style="max-width: 420px">
      <!-- Branded Header -->
      <div class="text-center q-mb-xl">
        <h2 class="text-heading text-navy no-margin">SAMS<span class="text-primary">.</span></h2>
        <div class="text-overline text-grey-6 letter-spacing-5">Secure Access Gateway</div>
      </div>

      <!-- Professional Login Card -->
      <q-card flat bordered class="sams-card full-width q-pa-xl">
        <div class="text-center q-mb-xl">
           <div class="text-h5 text-heading text-navy uppercase">{{ targetRole }} Sign In</div>
           <div class="text-caption text-grey-6 q-mt-sm">Access your academy dashboard</div>
        </div>

        <div class="q-gutter-y-lg">
          <q-input
            v-model="loginData.username"
            label="Username"
            outlined
            color="primary"
            class="sams-input"
          >
            <template v-slot:prepend>
              <q-icon name="person_outline" color="grey-6" />
            </template>
          </q-input>

          <q-input
            v-model="loginData.password"
            label="Password"
            type="password"
            outlined
            color="primary"
            class="sams-input"
            @keyup.enter="handleLogin"
          >
            <template v-slot:prepend>
              <q-icon name="lock_outline" color="grey-6" />
            </template>
          </q-input>
        </div>

        <div class="q-mt-xl">
          <q-btn
            unelevated
            class="full-width q-py-md sams-btn-action"
            label="Sign In"
            :loading="loading"
            @click="handleLogin"
          />
        </div>

        <div class="text-center q-mt-xl">
          <q-btn flat color="grey-7" label="Back to Home" to="/" icon="arrow_back" dense no-caps />
        </div>
      </q-card>

      <!-- Trust Footer -->
      <div class="row items-center q-mt-xl q-gutter-sm opacity-40">
         <q-icon name="verified_user" size="18px" />
         <span class="text-caption text-weight-bold uppercase">Enterprise Security Active</span>
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
    $q.notify({
      message: error.response?.data?.detail || 'Invalid credentials.',
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
.sams-auth {
  background-color: var(--sams-bg);
  min-height: 100vh;
}

.sams-input {
  :deep(.q-field__control) {
    border-radius: 12px;
  }
}

.letter-spacing-5 { letter-spacing: 5px; }
.opacity-40 { opacity: 0.4; }
</style>
