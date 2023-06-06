import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
      { find: '@', replacement: '/src' },
      { find: 'app', replacement: '/src/app' },
      { find: 'assets', replacement: '/src/assets' },
      { find: 'components', replacement: '/src/components' },
      { find: 'context', replacement: '/src/context' },
      { find: 'data', replacement: '/src/data' },
      { find: 'features', replacement: '/src/features' },
      { find: 'layouts', replacement: '/src/layouts' },
      { find: 'lib', replacement: '/src/lib' },
      { find: 'pages', replacement: '/src/pages' },
      { find: 'services', replacement: '/src/services' },
      { find: 'utils', replacement: '/src/utils' },
      { find: 'server', replacement: '/src/server' },
    ],
  },
  server: {
    watch: {
        usePolling: true
    },
    host: "0.0.0.0",
    port: 3000,
  }
})
