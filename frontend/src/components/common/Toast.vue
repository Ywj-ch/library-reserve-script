<template>
  <div class="fixed right-4 top-4 z-50 space-y-2">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'flex max-w-sm items-center rounded-lg px-4 py-3 shadow-lg backdrop-blur-md',
          toastClasses[toast.type],
        ]"
      >
        <div class="mr-3">
          <CheckCircleIcon v-if="toast.type === 'success'" class="w-6 h-6" />
          <XCircleIcon v-else-if="toast.type === 'error'" class="w-6 h-6" />
          <ExclamationTriangleIcon v-else-if="toast.type === 'warning'" class="w-6 h-6" />
          <InformationCircleIcon v-else class="w-6 h-6" />
        </div>
        <div class="flex-1 text-sm font-medium">{{ toast.message }}</div>
        <button
          @click="removeToast(toast.id)"
          class="ml-3 text-lg opacity-70 hover:opacity-100 transition-opacity"
        >
          <XMarkIcon class="w-5 h-5" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useToastStore } from '@/stores/toast'
import {
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XMarkIcon,
} from '@heroicons/vue/24/outline'

const toastStore = useToastStore()
const toasts = computed(() => toastStore.toasts)
const removeToast = toastStore.removeToast

const toastClasses = {
  success: 'bg-green-50/90 dark:bg-green-900/30 text-green-900 dark:text-green-100 border border-green-200 dark:border-green-700/50',
  error: 'bg-red-50/90 dark:bg-red-900/30 text-red-900 dark:text-red-100 border border-red-200 dark:border-red-700/50',
  warning: 'bg-yellow-50/90 dark:bg-yellow-900/30 text-yellow-900 dark:text-yellow-100 border border-yellow-200 dark:border-yellow-700/50',
  info: 'bg-blue-50/90 dark:bg-blue-900/30 text-blue-900 dark:text-blue-100 border border-blue-200 dark:border-blue-700/50',
}
</script>

<style scoped>
.toast-enter-active {
  animation: slide-in 0.3s ease-out;
}

.toast-leave-active {
  animation: slide-out 0.3s ease-in;
}

@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slide-out {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}
</style>
