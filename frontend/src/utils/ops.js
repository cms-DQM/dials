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

const buildTree = (items) => {
  const tree = []
  items.forEach((item) => {
    const path = item.me
    const parts = path.split('/')
    let currentLevel = tree
    parts.forEach((part, index) => {
      let existingPath = currentLevel.find((node) => node.name === part)
      if (!existingPath) {
        existingPath = {
          name: part,
          type: index === parts.length - 1 ? 'file' : 'directory',
          children: [],
          me_id: index === parts.length - 1 ? item.me_id : undefined,
          count: index === parts.length - 1 ? item.count : undefined,
          dim: index === parts.length - 1 ? item.dim : undefined,
        }
        currentLevel.push(existingPath)
      }
      currentLevel = existingPath.children
    })
  })
  return tree
}

export { groupBySplitME, buildTree }
