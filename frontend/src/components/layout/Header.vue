<template>
  <header class="fixed top-4 left-4 right-4 z-50">
    <div class="glass-card py-4 px-6">
      <div class="flex items-center justify-between max-w-7xl mx-auto">
        <div class="flex items-center space-x-3">
          <BookOpenIcon class="w-8 h-8 text-primary" />
          <h1 class="text-xl font-semibold text-gray-900 dark:text-gray-100">图书馆座位预约助手</h1>
        </div>
        <nav class="flex items-center space-x-4">
          <router-link
            to="/"
            class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 transition-all duration-200 hover:text-primary rounded-lg hover:bg-white/50 dark:hover:bg-white/10"
            :class="{ 'text-primary bg-white/50 dark:bg-white/10': $route.path === '/' }"
          >
            仪表板
          </router-link>
          <router-link
            to="/logs"
            class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 transition-all duration-200 hover:text-primary rounded-lg hover:bg-white/50 dark:hover:bg-white/10"
            :class="{ 'text-primary bg-white/50 dark:bg-white/10': $route.path === '/logs' }"
          >
            日志记录
          </router-link>
          <ThemeToggle />
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { BookOpenIcon } from '@heroicons/vue/24/outline'
import ThemeToggle from './ThemeToggle.vue'
</script>
