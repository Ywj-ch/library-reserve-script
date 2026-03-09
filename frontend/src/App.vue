<template>
  <div class="min-h-screen bg-transparent flex flex-col transition-colors duration-300">
    <Header />
    <main class="container mx-auto px-4 py-6 flex-1">
      <router-view />
    </main>
    <footer class="glass-card border-t border-white/20 dark:border-white/10 py-4 mt-auto rounded-none">
      <div class="container mx-auto px-4 text-center">
        <p class="text-sm text-gray-700 dark:text-gray-300">
          Copyright © {{ currentYear }} 
          <span class="font-medium text-primary">chippanda</span>
        </p>
      </div>
    </footer>
    <Toast />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Header from '@/components/layout/Header.vue'
import Toast from '@/components/common/Toast.vue'

const currentYear = computed(() => new Date().getFullYear())
</script>
