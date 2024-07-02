const toUndefined = (value, pattern) => (value === pattern ? undefined : value)

const isNumericNonZero = (num) => {
  return !isNaN(num) && +num > 0
}

const isStringNonEmpty = (str) => {
  return str !== '' && str !== null && str !== undefined
}

const sanitizedURLSearchParams = (values, { repeatMode }) => {
  const params = new URLSearchParams()
  Object.entries(values).forEach(([key, value]) => {
    if (repeatMode && Array.isArray(value)) {
      value.forEach((elem) => params.append(key, elem))
    } else {
      params.append(key, value)
    }
  })

  const keysForDel = []
  params.forEach((value, key) => {
    if (
      value === '' ||
      value === 'undefined' ||
      value === 'null' ||
      value === undefined ||
      values === null
    ) {
      keysForDel.push(key)
    }
  })
  keysForDel.forEach((key) => {
    params.delete(key)
  })
  return params
}

const getNextToken = (response, key) => {
  return response[[key]]
    ? new URLSearchParams(response[[key]].split('?')[1]).get('next_token')
    : null
}

const pathsToJson = (paths) => {
  const result = {}
  paths.forEach((path) => {
    const parts = path.split('/')
    let currentLevel = result

    parts.forEach((part, index) => {
      if (!currentLevel[part]) {
        if (index === parts.length - 1) {
          currentLevel[part] = null
        } else {
          currentLevel[part] = {}
        }
      }
      currentLevel = currentLevel[part]
    })
  })

  return result
}

export {
  toUndefined,
  isNumericNonZero,
  isStringNonEmpty,
  sanitizedURLSearchParams,
  getNextToken,
  pathsToJson,
}
