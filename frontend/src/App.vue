<template>
  <div class="flex min-h-screen flex-col bg-transparent transition-colors duration-300">
    <Header />
    <main class="container mx-auto flex-1 px-4 py-6">
      <router-view />
    </main>
    <footer
      class="glass-card mt-auto rounded-none border-t border-white/20 py-4 dark:border-white/10"
    >
      <div class="container mx-auto px-4 text-center">
        <p class="text-sm text-gray-700 dark:text-gray-300">
          Copyright © {{ currentYear }}
          <a
            href="https://www.chippanda.top/"
            target="_blank"
            rel="noopener noreferrer"
            class="font-medium text-primary hover:underline"
            >chippanda</a
          >
        </p>
      </div>
    </footer>
    <Toast />
    <MagicPlant />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Header from '@/components/layout/Header.vue'
import Toast from '@/components/common/Toast.vue'
// import MagicPlant from '@/components/business/MagicPlant.vue'

const currentYear = computed(() => new Date().getFullYear())
</script>
