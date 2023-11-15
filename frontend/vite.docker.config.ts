import react from '@vitejs/plugin-react';
import { checker } from 'vite-plugin-checker';
import { defineConfig } from 'vitest/config';
import { loadEnv } from 'vite';

let hostValue: string;
let portValue: number;
const envDir = '../.envs';

export default defineConfig(({ mode }) => {
  if (process.env.NODE_ENV === 'docker') {
    mode = 'docker';
    process.env = loadEnv(mode, `${envDir}/react.env`, '');
    hostValue = process.env.HOST.toString();
    portValue = Number(process.env.PORT);
  }
  return {
    plugins: [react(), checker({ typescript: true })],
    build: {
      outDir: 'build_production',
    },
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
      host: hostValue,
      port: portValue,
    },
    define: {
      'process.env': process.env,
    },
    optimizeDeps: {
      include: ['web-vitals'],
    },
  };
});
