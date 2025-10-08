import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: ['antd'] // Явное включение antd в предварительную обработку
  },
  server.allowedHosts: {
    host: '0.0.0.0', // Это заставит сервер разработки слушать только localhost
    port: 5173,        // Опционально: можно указать конкретный порт, если нужно
  }
})
