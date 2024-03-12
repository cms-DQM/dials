const path = require('path')

const basePath = 'frontend'

module.exports = {
  paths: function (paths, env) {
    paths.appIndexJs = path.resolve(__dirname, `${basePath}/src/index.js`)
    paths.appSrc = path.resolve(__dirname, `${basePath}/src`)
    paths.appPublic = path.resolve(__dirname, `${basePath}/public`)
    paths.appHtml = path.resolve(__dirname, `${basePath}/public/index.html`)
    return paths
  }
}
