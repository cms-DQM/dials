import { format } from 'date-fns'

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

const formatDate = (date, fmt) => {
  if (!date) {
    return ''
  }
  fmt = fmt || 'dd/MM/yyyy'
  return format(new Date(date), fmt)
}

const groupBySplitME = (data) => {
  const groupedData = data.reduce((acc, item) => {
    const [firstPart, secondPart] = item.me.split('/')
    const key = `${firstPart}/${secondPart.split('/')[0]}`

    if (!acc[key]) {
      acc[key] = {
        me: key,
        count: item.count,
      }
    } else {
      acc[key].count += item.count
    }

    return acc
  }, {})

  return Object.values(groupedData)
}

const listToRange = function* (arr) {
  const groups = []
  let currentGroup = []

  for (const [, value] of arr.entries()) {
    if (
      currentGroup.length === 0 ||
      value - currentGroup[currentGroup.length - 1] === 1
    ) {
      currentGroup.push(value)
    } else {
      groups.push(currentGroup)
      currentGroup = [value]
    }
  }
  if (currentGroup.length > 0) {
    groups.push(currentGroup)
  }

  for (const group of groups) {
    yield [group[0], group[group.length - 1]]
  }
}

const rangeToList = (ranges) => {
  const result = []

  for (const [start, end] of ranges) {
    for (let i = start; i <= end; i++) {
      result.push(i)
    }
  }

  return result
}

export {
  toUndefined,
  isNumericNonZero,
  isStringNonEmpty,
  sanitizedURLSearchParams,
  getNextToken,
  formatDate,
  groupBySplitME,
  listToRange,
  rangeToList,
}
