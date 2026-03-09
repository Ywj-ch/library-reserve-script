import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/styles/main.css'
import { useThemeStore } from './stores/theme'

// ============================================
// 全局主题初始化（不依赖 Vue 组件生命周期）
// ============================================
const THEME_KEY = 'library-reserve-theme'

function getSystemPreference() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function loadSavedTheme() {
  try {
    const saved = localStorage.getItem(THEME_KEY)
    if (saved === 'light' || saved === 'dark') {
      return saved
    }
  } catch (err) {
    console.warn('读取主题设置失败:', err)
  }
  return 'light'
}

function applyTheme(mode: 'light' | 'dark') {
  const html = document.documentElement
  html.setAttribute('data-theme', mode)

  // 同时设置 dark 类名，用于 Tailwind
  if (mode === 'dark') {
    html.classList.add('dark')
  } else {
    html.classList.remove('dark')
  }
}

function initTheme() {
  const mode = loadSavedTheme()
  applyTheme(mode)
}

// 初始化主题
initTheme()

// ============================================
// Vue 应用初始化
// ============================================
const app = createApp(App)

app.use(createPinia())
app.use(router)

// 初始化 Pinia store 中的主题状态
const themeStore = useThemeStore()
themeStore.initTheme()

app.mount('#app')
