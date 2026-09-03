import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'node:url'

export default defineConfig(({ mode }) => {
  const rootEnv = loadEnv(
    mode,
    fileURLToPath(new URL('../', import.meta.url)),
    '',
  )

  const apiKeyHeaders = rootEnv.DATA_API_KEY
    ? { 'x-api-key': rootEnv.DATA_API_KEY }
    : {}

  return {
    plugins: [react()],
    server: {
      port: 5173,
      proxy: {
        '/predict': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          headers: apiKeyHeaders,
        },
        '/scans': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
        },
                '/collection-points': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
        },
        '/stats': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
        },
      },
    },
  }
})
