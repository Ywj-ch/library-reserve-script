<template>
  <button
    @click="toggleTheme"
    class="relative p-2 rounded-lg glass-card hover:scale-105 transition-all duration-200"
    :title="theme === 'light' ? '切换到暗色模式' : '切换到亮色模式'"
  >
    <transition name="theme-icon" mode="out-in">
      <SunIcon
        v-if="theme === 'dark'"
        key="sun"
        class="w-5 h-5 text-yellow-400"
      />
      <MoonIcon
        v-else
        key="moon"
        class="w-5 h-5 text-primary"
      />
    </transition>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { SunIcon, MoonIcon } from '@heroicons/vue/24/outline'

const themeStore = useThemeStore()
const theme = computed(() => themeStore.theme)
const toggleTheme = () => themeStore.toggleTheme()
</script>

<style scoped>
.theme-icon-enter-active,
.theme-icon-leave-active {
  transition: all 0.2s ease;
}

.theme-icon-enter-from {
  opacity: 0;
  transform: rotate(-90deg) scale(0.5);
}

.theme-icon-leave-to {
  opacity: 0;
  transform: rotate(90deg) scale(0.5);
}
</style>
