import { getNextToken } from '../../utils/sanitizer'

const genericFetchAllPages = async ({ apiMethod, params = {} }) => {
  const allData = []
  let nextPageExists = true
  let nextToken = null
  let errorCount = 0
  let totalPages = 0
  while (nextPageExists) {
    totalPages++
    try {
      const { results, next } = await apiMethod({
        nextToken,
        ...params,
      })
      results.forEach((e) => allData.unshift(e))
      nextPageExists = !(next === null)
      nextToken = getNextToken({ next }, 'next')
    } catch (err) {
      errorCount++
    }
  }

  return {
    results: allData,
    count: allData.length,
    error: errorCount,
    totalPages,
  }
}

const utilsApi = {
  utils: {
    genericFetchAllPages,
  },
}

export default utilsApi
