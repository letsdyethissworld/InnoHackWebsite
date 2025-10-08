import { defineConfig } from 'vite'
import path from 'path'

export default defineConfig({
  // ... другие настройки
  resolve: {
    alias: {
      antd: path.join(__dirname, 'node_modules/antd/dist/antd.js')
    }
  }
})
