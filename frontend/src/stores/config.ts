import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Config, DatetimeRange } from '@/types/config'
import type { SystemStatus } from '@/types/api'
import { configApi } from '@/api/config'
import { statusApi } from '@/api/status'

export const useConfigStore = defineStore('config', () => {
  const config = ref<Config | null>(null)
  const status = ref<SystemStatus | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchConfig() {
    try {
      loading.value = true
      error.value = null
      const response = await configApi.getFullConfig()
      if (response.success) {
        config.value = response.data
      }
    } catch (e: any) {
      error.value = e.message || '获取配置失败'
      console.error('Failed to fetch config:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchStatus() {
    try {
      const response = await statusApi.getStatus()
      if (response.success) {
        status.value = response.data
      }
    } catch (e: any) {
      console.error('Failed to fetch status:', e)
    }
  }

  async function updateAuth(cookie: string, code: string) {
    try {
      loading.value = true
      error.value = null
      const response = await configApi.updateAuthConfig({ cookie, code })
      if (response.success) {
        await fetchConfig()
        await fetchStatus()
        return true
      }
      return false
    } catch (e: any) {
      error.value = e.message || '更新认证配置失败'
      return false
    } finally {
      loading.value = false
    }
  }

  async function updateReserve(sendTime: string, seats: any[], datetimeRange?: DatetimeRange) {
    try {
      loading.value = true
      error.value = null
      const response = await configApi.updateReserveConfig({
        send_time: sendTime,
        seats,
        datetime_range: datetimeRange,
      })
      if (response.success) {
        await fetchConfig()
        return true
      }
      return false
    } catch (e: any) {
      error.value = e.message || '更新预约配置失败'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    config,
    status,
    loading,
    error,
    fetchConfig,
    fetchStatus,
    updateAuth,
    updateReserve,
  }
})
