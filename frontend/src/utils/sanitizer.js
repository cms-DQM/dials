const toUndefined = (value, pattern) => value === pattern ? undefined : value

const isNumericNonZero = (num) => {
  return !isNaN(num) && +num > 0
}

const isStringNonEmpty = (str) => {
  return str !== '' && str !== null && str !== undefined
}

export {
  toUndefined,
  isNumericNonZero,
  isStringNonEmpty
}
