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

export { groupBySplitME }
