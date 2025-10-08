import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: ['antd'] // Явное включение antd в предварительную обработку
  },
  server: {
    host: 'localhost', // Это заставит сервер разработки слушать только localhost
    port: 3000,        // Опционально: можно указать конкретный порт, если нужно
  }
})
