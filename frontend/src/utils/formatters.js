function isEmptyValue(value) {
  return value === undefined || value === null || value === ''
}

function toNumber(value) {
  if (isEmptyValue(value)) {
    return null
  }

  const numberValue = Number(value)

  return Number.isFinite(numberValue) ? numberValue : null
}

export function formatRupiah(value) {
  const numberValue = toNumber(value)

  if (numberValue === null) {
    return '-'
  }

  return `Rp${new Intl.NumberFormat('id-ID', {
    maximumFractionDigits: 0,
  }).format(numberValue)}`
}

export function formatOriginalPrice(priceOriginal, priceCurrency) {
  const numberValue = toNumber(priceOriginal)

  if (numberValue === null || isEmptyValue(priceCurrency)) {
    return '-'
  }

  return `Harga asli dataset: ${new Intl.NumberFormat('id-ID').format(numberValue)} ${priceCurrency}`
}

export function formatPrice(value) {
  if (value && typeof value === 'object') {
    if (toNumber(value.price_idr) !== null) {
      return formatRupiah(value.price_idr)
    }

    return 'Harga belum tersedia'
  }

  return formatRupiah(value)
}

export function formatRating(value) {
  const numberValue = toNumber(value)

  if (numberValue === null) {
    return '-'
  }

  return numberValue.toFixed(1)
}

export function formatConfidence(value) {
  const numberValue = toNumber(value)

  if (numberValue === null) {
    return '-'
  }

  const percentage = numberValue <= 1 ? numberValue * 100 : numberValue

  return `${percentage.toFixed(1)}%`
}

export function formatScore(value) {
  const numberValue = toNumber(value)

  if (numberValue === null) {
    return '-'
  }

  return numberValue.toFixed(2)
}

export function formatCompactScore(value) {
  const numberValue = toNumber(value)

  if (numberValue === null) {
    return '-'
  }

  return Number(numberValue.toFixed(3)).toString()
}

export function normalizeOption(value) {
  if (isEmptyValue(value)) {
    return '-'
  }

  return String(value).trim() || '-'
}

export function buildLaptopSpecText(laptop) {
  if (!laptop || typeof laptop !== 'object') {
    return '-'
  }

  const specs = [
    laptop.processor || laptop.cpu,
    laptop.ram,
    laptop.storage,
    laptop.gpu,
  ]
    .map(normalizeOption)
    .filter((value) => value !== '-')

  return specs.length ? specs.join(' | ') : '-'
}
