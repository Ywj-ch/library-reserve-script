<template>
  <header class="border-b border-gray-200 bg-white">
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <span class="text-2xl">📚</span>
          <h1 class="text-xl font-semibold text-gray-900">图书馆座位预约助手</h1>
        </div>
        <nav class="flex items-center space-x-4">
          <router-link
            to="/"
            class="px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:text-primary"
            :class="{ 'text-primary': $route.path === '/' }"
          >
            仪表板
          </router-link>
          <router-link
            to="/logs"
            class="px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:text-primary"
            :class="{ 'text-primary': $route.path === '/logs' }"
          >
            日志记录
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts"></script>
