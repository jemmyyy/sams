import { ref, type Ref } from 'vue'
import { useI18n } from 'vue-i18n'

type RulesFn = (v: unknown) => true | string

export function useFormValidation() {
  const { t } = useI18n()

  const required = (label: string): RulesFn[] => [
    (v: unknown) => (!!v && v !== '') || t('validation.required', { field: label }),
  ]

  const email: RulesFn[] = [
    (v: unknown) => {
      if (!v) return true
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return re.test(String(v)) || t('validation.email')
    },
  ]

  const minLength = (min: number): RulesFn[] => [
    (v: unknown) => {
      if (!v) return true
      return String(v).length >= min || t('validation.minLength', { n: min })
    },
  ]

  const phone: RulesFn[] = [
    (v: unknown) => {
      if (!v) return true
      const re = /^\+?[\d\s\-()]{7,20}$/
      return re.test(String(v)) || t('validation.phone')
    },
  ]

  const passwordMatch = (passwordRef: Ref<string>): RulesFn[] => [
    (v: unknown) => v === passwordRef.value || t('validation.passwordMatch'),
  ]

  return { required, email, minLength, phone, passwordMatch }
}
