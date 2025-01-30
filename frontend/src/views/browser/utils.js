export const buildTree = (items) => {
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
