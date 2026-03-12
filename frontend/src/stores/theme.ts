import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export type Theme = 'light' | 'dark'

const THEME_KEY = 'library-reserve-theme'

export const useThemeStore = defineStore('theme', () => {
  const theme = ref<Theme>('light')

  function initTheme() {
    // 从 localStorage 读取或从 DOM 获取已应用的主题
    const savedTheme = localStorage.getItem(THEME_KEY) as Theme | null
    const htmlTheme = document.documentElement.getAttribute('data-theme') as Theme | null

    if (htmlTheme) {
      theme.value = htmlTheme
    } else if (savedTheme) {
      theme.value = savedTheme
      applyTheme(savedTheme)
    } else {
      theme.value = 'light'
      applyTheme('light')
    }
  }

  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    applyTheme(theme.value)
    localStorage.setItem(THEME_KEY, theme.value)
  }

  function applyTheme(newTheme: Theme) {
    const html = document.documentElement

    // 设置 data-theme 属性（用于 CSS 变量方案）
    html.setAttribute('data-theme', newTheme)

    // 同时设置 dark 类名（用于 Tailwind）
    if (newTheme === 'dark') {
      html.classList.add('dark')
    } else {
      html.classList.remove('dark')
    }
  }

  watch(theme, (newTheme) => {
    applyTheme(newTheme)
  })

  return {
    theme,
    initTheme,
    toggleTheme,
  }
})
