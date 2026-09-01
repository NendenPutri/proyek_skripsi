const variantClasses = {
  success: 'badge-success',
  warning: 'badge-warning',
  muted: 'badge-muted',
  default: 'badge-muted',
}

function Badge({ children, variant = 'default', className = '', ...props }) {
  const badgeClass = `badge ${variantClasses[variant] || variantClasses.default} ${className}`.trim()

  return (
    <span className={badgeClass} {...props}>
      {children}
    </span>
  )
}

export default Badge
