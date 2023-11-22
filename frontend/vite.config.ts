/// <reference types="vitest" />
import react from '@vitejs/plugin-react';
import { checker } from 'vite-plugin-checker';
import { defineConfig } from 'vitest/config';
import dotenv from 'dotenv';

let hostValue: string;
let portValue: number;

const alias = [
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
  { find: 'tests', replacement: '/src/tests' },
];
dotenv.config({ path: '../.envs/react.env' });

if (process.env.HOST && process.env.PORT) {
  hostValue = process.env.HOST;
  portValue = Number(process.env.PORT);
} else {
  hostValue = '0.0.0.0';
  portValue = 3000;
}

export default defineConfig({
  plugins: [react(), checker({ typescript: true })],
  resolve: {
    alias: [...alias],
  },
  test: {
    environment: 'jsdom',
    setupFiles: './vitest-setup.ts',
    coverage: {
      lines: 60,
      branches: 60,
      functions: 60,
      statements: 60,
      provider: 'v8',
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
});
