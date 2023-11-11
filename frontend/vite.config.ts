import react from '@vitejs/plugin-react';
import { checker } from 'vite-plugin-checker';
import { defineConfig } from 'vitest/config';
import { loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '../.envs/react.env', '');
  return {
    plugins: [react(), checker({ typescript: true })],
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
        { find: 'repositories', replacement: '/src/repositories' },
        { find: 'utils', replacement: '/src/utils' },
        { find: 'server', replacement: '/src/server' },
        { find: 'types', replacement: '/src/types' },
        { find: 'styles', replacement: '/src/styles' },
        { find: 'constants', replacement: '/src/constants' },
      ],
    },
    test: {
      globals: true,
      setupFiles: './vitest-setup.tsx',
      environment: 'jsdom',
      coverage: {
        lines: 60,
        branches: 60,
        functions: 60,
        statements: 60,
        provider: 'c8',
        reporter: ['text', 'json-summary', 'json', 'lcov'],
      },
    },
    server: {
      watch: {
        usePolling: true,
      },
      host: env.HOST,
      port: Number(env.PORT),
    },
    define: {
      'process.env': env,
    },
    optimizeDeps: {
      include: ['web-vitals'],
    },
  };
});
