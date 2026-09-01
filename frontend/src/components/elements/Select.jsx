function normalizeSelectOption(option) {
  if (typeof option !== 'object' || option === null) {
    return {
      label: String(option),
      value: option,
    }
  }

  return {
    label: option.label ?? String(option.value ?? ''),
    value: option.value ?? option.label ?? '',
  }
}

function Select({
  label,
  name,
  value,
  onChange,
  options = [],
  error,
  helper,
  className = '',
  ...props
}) {
  const selectId = props.id || name

  return (
    <div className={className}>
      {label ? (
        <label className="label-field" htmlFor={selectId}>
          {label}
        </label>
      ) : null}
      <select
        className="select-field"
        id={selectId}
        name={name}
        onChange={onChange}
        value={value}
        {...props}
      >
        {options.map((option) => {
          const normalizedOption = normalizeSelectOption(option)

          return (
            <option key={normalizedOption.value} value={normalizedOption.value}>
              {normalizedOption.label}
            </option>
          )
        })}
      </select>
      {error ? <p className="field-error">{error}</p> : null}
      {!error && helper ? <p className="field-helper">{helper}</p> : null}
    </div>
  )
}

export default Select
