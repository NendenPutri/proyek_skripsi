function Input({
  label,
  name,
  type = 'text',
  value,
  onChange,
  placeholder,
  min,
  max,
  error,
  helper,
  className = '',
  ...props
}) {
  const inputId = props.id || name

  return (
    <div className={className}>
      {label ? (
        <label className="label-field" htmlFor={inputId}>
          {label}
        </label>
      ) : null}
      <input
        className="input-field"
        id={inputId}
        max={max}
        min={min}
        name={name}
        onChange={onChange}
        placeholder={placeholder}
        type={type}
        value={value}
        {...props}
      />
      {error ? <p className="field-error">{error}</p> : null}
      {!error && helper ? <p className="field-helper">{helper}</p> : null}
    </div>
  )
}

export default Input
