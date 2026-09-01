const variantClasses = {
  primary: 'btn-primary',
  secondary: 'btn-secondary',
  ghost: 'btn-ghost',
}

function Button({
  children,
  variant = 'primary',
  type = 'button',
  disabled = false,
  className = '',
  ...props
}) {
  const buttonClass = `btn ${variantClasses[variant] || variantClasses.primary} ${className}`.trim()

  return (
    <button className={buttonClass} disabled={disabled} type={type} {...props}>
      {children}
    </button>
  )
}

export default Button
