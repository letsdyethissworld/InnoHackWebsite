import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      // Явно указываем, что antd не является внешней зависимостью
      external: ['antd']
    }
  }
})
