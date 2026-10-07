import clsx from 'clsx'

export default function Badge({ children, variant = 'default', className }) {
  const variants = {
    default: 'bg-gray-100 text-gray-800',
    primary: 'bg-blue-100 text-blue-800',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    danger: 'bg-red-100 text-red-800',
    purple: 'bg-purple-100 text-purple-800',
  }

  const statusVariants = {
    AVAILABLE: 'success',
    APPLIED: 'primary',
    SHORTLISTED: 'primary',
    SELECTED: 'success',
    PROCESSING: 'warning',
    UNAVAILABLE: 'danger',
    DEPLOYED: 'success',
    BLOCKED: 'danger',
    ARCHIVED: 'default',
  }

  // Auto-detect status variant
  const finalVariant = statusVariants[children] || variant

  return (
    <span
      className={clsx(
        'inline-block px-2 py-1 rounded-full text-xs font-semibold',
        variants[finalVariant],
        className
      )}
    >
      {children}
    </span>
  )
}