// ── Shared TypeScript interfaces ──

export interface Academy {
  id: string
  name: string
  subscription_plan: 'free' | 'basic' | 'premium' | 'enterprise'
  status: 'active' | 'suspended' | 'trialing' | 'cancelled'
  timezone: string
  language: string
  currency: string
}

export interface User {
  id: string
  username: string
  email: string
  phone_number: string
  first_name: string
  last_name: string
  preferred_language: 'en' | 'ar'
}

export interface UserRole {
  id: string
  user: string
  academy: string
  role: 'customer' | 'coach' | 'operations' | 'admin' | 'super_admin'
}

export interface Player {
  id: string
  academy: string
  first_name: string
  last_name: string
  birth_date: string
  registration_number: string
  email: string
  phone_number: string
  status: 'active' | 'inactive'
  photo: string | null
  gender: 'male' | 'female' | 'other' | ''
  medical_notes: string
  emergency_contact: EmergencyContact | null
  parent_id: string | null
  created_at: string
  updated_at: string
}

export interface EmergencyContact {
  name: string
  relationship: string
  phone_number: string
  email?: string
}

export interface Coach {
  id: string
  academy: string
  user: User
  specializations: string[]
  certifications: Certification[]
  bio: string
  hire_date: string | null
  is_active: boolean
  max_weekly_hours: number
  availabilities: CoachAvailability[]
}

export interface Certification {
  name: string
  issuer: string
  date_obtained: string
  expiry_date?: string
}

export interface CoachAvailability {
  id: string
  coach: string
  day_of_week: number
  start_time: string
  end_time: string
  is_active: boolean
}

export interface SessionSeries {
  id: string
  academy: string
  title: string
  description: string
  start_date: string
  end_date: string | null
  start_time: string
  end_time: string
  recurrence_rule: string
  venue: Venue | { id: string; name: string }
  max_capacity: number
  is_active: boolean
}

export interface SessionOccurrence {
  id: string
  academy: string
  series: SessionSeries | { id: string; title: string }
  start_datetime: string
  end_datetime: string
  venue: Venue | { id: string; name: string }
  max_capacity: number
  status: 'scheduled' | 'cancelled' | 'completed'
  cancellation_reason: string
}

export interface SessionCoach {
  id: string
  session: string
  coach: string
  is_lead: boolean
}

export interface Enrollment {
  id: string
  session: string
  player: string
  enrolled_at: string
  status: 'active' | 'cancelled' | 'attended' | 'missed'
}

export interface Venue {
  id: string
  academy: string
  name: string
  location: string
  capacity: number
  is_active: boolean
}

export interface Attendance {
  id: string
  session: string
  player: string
  status: 'present' | 'absent' | 'late' | 'excused'
  marked_by: string | null
  marked_at: string | null
  notes: string
}

export interface Rating {
  id: string
  session: string
  coach: string
  player: string
  score: number
  category: string
  notes: string
  created_at: string
}

export interface Payment {
  id: string
  academy: string
  player: string
  amount: string
  payment_type: 'cash' | 'bank_transfer' | 'card'
  status: 'pending' | 'completed' | 'failed' | 'refunded'
  payment_date: string | null
  reference_number: string
  notes: string
  created_at: string
}

export interface Invoice {
  id: string
  academy: string
  player: string
  amount: string
  status: 'pending' | 'paid' | 'partially_paid' | 'overdue' | 'cancelled'
  due_date: string
  issued_date: string
  description: string
  discount: string | null
  coupon: string | null
}

export interface Notification {
  id: string
  academy: string
  recipient: string
  channel: 'push' | 'email' | 'sms'
  title: string
  body: string
  is_read: boolean
  sent_at: string
  read_at: string | null
}

export interface Group {
  id: string
  academy: string
  name: string
  description: string
  players: string[]
  coach: string | null
  is_active: boolean
}

export interface ApiResponse<T> {
  success: boolean
  data: T
  errors: Record<string, string[]> | null
  message: string
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface LoginCredentials {
  username: string
  password: string
  academy_id: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  password_confirm: string
  first_name: string
  last_name: string
  phone_number: string
  academy_name?: string
}

export interface AuthTokens {
  access: string
  refresh: string
}

export type PortalRole = 'customer' | 'coach' | 'operations' | 'admin' | 'super_admin'

export interface NavItem {
  label: string
  icon: string
  to: string
  roles: PortalRole[]
  children?: NavItem[]
}
