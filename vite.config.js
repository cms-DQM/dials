import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import svgr from 'vite-plugin-svgr'
import eslint from 'vite-plugin-eslint'

const isDocker = process.env.DOCKERIZED
const rootPath = './frontend'

export default defineConfig(() => {
  return {
    root: rootPath,
    server: {
      open: !isDocker,
      port: 3000
    },
    build: {
      outDir: 'build'
    },
    plugins: [
      react(),
      svgr({ svgrOptions: { icon: true } }),
      eslint()
    ]
  }
})
