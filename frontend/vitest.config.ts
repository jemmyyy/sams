import { defineConfig } from 'vitest/config'
import { resolve } from 'path'

export default defineConfig({
  resolve: {
    alias: {
      src: resolve(__dirname, 'src'),
      'src/': resolve(__dirname, 'src') + '/',
      components: resolve(__dirname, 'src/components'),
      'components/': resolve(__dirname, 'src/components') + '/',
      layouts: resolve(__dirname, 'src/layouts'),
      'layouts/': resolve(__dirname, 'src/layouts') + '/',
      pages: resolve(__dirname, 'src/pages'),
      'pages/': resolve(__dirname, 'src/pages') + '/',
      stores: resolve(__dirname, 'src/stores'),
      'stores/': resolve(__dirname, 'src/stores') + '/',
      boot: resolve(__dirname, 'src/boot'),
      'boot/': resolve(__dirname, 'src/boot') + '/',
      assets: resolve(__dirname, 'src/assets'),
      'assets/': resolve(__dirname, 'src/assets') + '/',
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test-setup.ts'],
    globals: true,
    include: ['src/**/*.spec.{ts,js}', 'src/**/*.test.{ts,js}'],
  },
})
