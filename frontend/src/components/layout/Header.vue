<template>
  <header class="fixed left-4 right-4 top-4 z-50">
    <div class="glass-card px-6 py-4">
      <div class="mx-auto flex max-w-7xl items-center justify-between">
        <div class="flex items-center space-x-3">
          <BookOpenIcon class="h-8 w-8 text-primary" />
          <h1 class="text-xl font-semibold text-gray-900 dark:text-gray-100">图书馆座位预约助手</h1>
        </div>
        <nav class="flex items-center space-x-4">
          <router-link
            to="/"
            class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 transition-all duration-200 hover:bg-white/50 hover:text-primary dark:text-gray-300 dark:hover:bg-white/10"
            :class="{ 'bg-white/50 text-primary dark:bg-white/10': $route.path === '/' }"
          >
            仪表板
          </router-link>
          <router-link
            to="/logs"
            class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 transition-all duration-200 hover:bg-white/50 hover:text-primary dark:text-gray-300 dark:hover:bg-white/10"
            :class="{ 'bg-white/50 text-primary dark:bg-white/10': $route.path === '/logs' }"
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
