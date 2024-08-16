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

export { listToRange, rangeToList }
