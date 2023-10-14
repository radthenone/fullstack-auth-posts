import react from '@vitejs/plugin-react';
import { checker } from 'vite-plugin-checker';
import { defineConfig } from 'vitest/config';

export default defineConfig({
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
        host: '0.0.0.0',
        port: 3000,
    },
});
