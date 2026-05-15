import { defineStore } from 'pinia';
import { useI18n } from 'vue-i18n';
import { Quasar } from 'quasar';

export const useAppStore = defineStore('app', {
  state: () => ({
    locale: localStorage.getItem('locale') || 'en-US',
  }),
  getters: {
    isRtl: (state) => state.locale === 'ar-EG',
  },
  actions: {
    setLocale(newLocale: string) {
      this.locale = newLocale;
      localStorage.setItem('locale', newLocale);
      
      // Update vue-i18n
      const { locale } = useI18n();
      locale.value = newLocale;

      // Update Quasar RTL
      Quasar.lang.set(newLocale === 'ar-EG' ? 'ar' : 'en-US');
    },
    toggleLocale() {
      this.setLocale(this.locale === 'en-US' ? 'ar-EG' : 'en-US');
    }
  }
});
