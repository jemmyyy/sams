type StatusMap = Record<string, { label: string; color: string }>

const PAYMENT_STATUS: StatusMap = {
  pending: { label: 'Pending', color: 'warning' },
  completed: { label: 'Completed', color: 'positive' },
  failed: { label: 'Failed', color: 'negative' },
  refunded: { label: 'Refunded', color: 'info' },
}

const INVOICE_STATUS: StatusMap = {
  pending: { label: 'Pending', color: 'warning' },
  paid: { label: 'Paid', color: 'positive' },
  partially_paid: { label: 'Partially Paid', color: 'info' },
  overdue: { label: 'Overdue', color: 'negative' },
  cancelled: { label: 'Cancelled', color: 'grey' },
}

const SESSION_STATUS: StatusMap = {
  scheduled: { label: 'Scheduled', color: 'info' },
  cancelled: { label: 'Cancelled', color: 'negative' },
  completed: { label: 'Completed', color: 'positive' },
}

const ENROLLMENT_STATUS: StatusMap = {
  active: { label: 'Active', color: 'positive' },
  cancelled: { label: 'Cancelled', color: 'negative' },
  attended: { label: 'Attended', color: 'info' },
  missed: { label: 'Missed', color: 'warning' },
}

const ATTENDANCE_STATUS: StatusMap = {
  present: { label: 'Present', color: 'positive' },
  absent: { label: 'Absent', color: 'negative' },
  late: { label: 'Late', color: 'warning' },
  excused: { label: 'Excused', color: 'info' },
}

export function getStatusLabel(map: StatusMap, key: string): string {
  return map[key]?.label ?? key
}

export function getStatusColor(map: StatusMap, key: string): string {
  return map[key]?.color ?? 'grey'
}

export {
  PAYMENT_STATUS,
  INVOICE_STATUS,
  SESSION_STATUS,
  ENROLLMENT_STATUS,
  ATTENDANCE_STATUS,
}
