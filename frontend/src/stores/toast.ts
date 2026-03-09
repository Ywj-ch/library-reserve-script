import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface ToastMessage {
  id: number
  message: string
  type: 'success' | 'error' | 'warning' | 'info'
  duration: number
}

export const useToastStore = defineStore('toast', () => {
  const toasts = ref<ToastMessage[]>([])
  let toastId = 0

  function addToast(message: string, type: ToastMessage['type'] = 'info', duration = 3000) {
    const id = ++toastId
    toasts.value.push({ id, message, type, duration })

    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }
  }

  function removeToast(id: number) {
    const index = toasts.value.findIndex((t) => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  function success(message: string, duration = 3000) {
    addToast(message, 'success', duration)
  }

  function error(message: string, duration = 5000) {
    addToast(message, 'error', duration)
  }

  function warning(message: string, duration = 4000) {
    addToast(message, 'warning', duration)
  }

  function info(message: string, duration = 3000) {
    addToast(message, 'info', duration)
  }

  return {
    toasts,
    addToast,
    removeToast,
    success,
    error,
    warning,
    info,
  }
})
