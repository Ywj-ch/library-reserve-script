<template>
  <div class="min-h-screen px-4 pb-8 pt-24">
    <div class="mx-auto max-w-7xl space-y-6">
      <div
        v-if="alertMessage"
        class="rounded-lg border-l-4 border-warning bg-yellow-50/90 p-4 backdrop-blur-sm dark:bg-yellow-900/20 dark:text-yellow-100"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <ExclamationTriangleIcon class="mr-3 h-8 w-8 text-warning" />
            <span class="font-medium">{{ alertMessage }}</span>
          </div>
          <Button @click="showUpdateModal = true" variant="primary" size="sm"> 立即更新 </Button>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-6 md:grid-cols-4">
        <Card>
          <div class="text-center">
            <CheckCircleIcon
              class="mx-auto mb-2 h-12 w-12"
              :class="statusColor === 'text-success' ? 'text-green-500' : 'text-yellow-500'"
            />
            <div class="mb-1 text-sm text-gray-600 dark:text-gray-400">服务状态</div>
            <div class="text-lg font-semibold" :class="statusColor">
              {{ statusText }}
            </div>
          </div>
        </Card>

        <Card>
          <div class="text-center">
            <ClockIcon class="mx-auto mb-2 h-12 w-12 text-primary" />
            <div class="mb-1 text-sm text-gray-600 dark:text-gray-400">下次运行</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {{ formatNextRun }}
            </div>
          </div>
        </Card>

        <Card>
          <div class="text-center">
            <ChartBarIcon class="mx-auto mb-2 h-12 w-12 text-primary" />
            <div class="mb-1 text-sm text-gray-600 dark:text-gray-400">成功率</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {{ status?.uptime_info?.success_rate || 0 }}%
            </div>
          </div>
        </Card>

        <Card>
          <div class="text-center">
            <PlayIcon class="mx-auto mb-2 h-12 w-12 text-primary" />
            <div class="mb-1 text-sm text-gray-600 dark:text-gray-400">手动执行</div>
            <Button
              @click="handleRunReserve"
              :loading="running"
              variant="primary"
              size="sm"
              class="mt-1"
            >
              立即运行
            </Button>
          </div>
        </Card>
      </div>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <ConfigPanel
          :cookie="config?.auth?.cookie || ''"
          :code="config?.auth?.code || ''"
          :last-update="config?.auth?.last_update || ''"
          :days-remaining="config?.auth?.days_remaining || 0"
          @save="handleAuthSave"
          @test="handleAuthTest"
        />

        <TimePicker
          :send-time="config?.reserve?.send_time || '07:00:02'"
          :datetime-range="config?.reserve?.datetime_range"
          :next-run="status?.next_run"
          :saving="saving"
          @save="handleTimeSave"
        />
      </div>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <SeatManager v-model="localSeats" :saving="saving" @save="handleSeatsSave" />

        <Card>
          <template #header>
            <div class="flex items-center space-x-3">
              <ClipboardDocumentListIcon class="h-6 w-6 text-primary" />
              <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">最近日志</h3>
            </div>
          </template>
          <template #actions>
            <router-link
              to="/logs"
              class="text-sm text-primary hover:text-blue-700 dark:hover:text-blue-400"
            >
              查看全部
            </router-link>
          </template>
          <div class="space-y-2">
            <div
              v-for="log in recentLogs"
              :key="log.timestamp"
              class="flex items-center justify-between border-b border-gray-100 py-2 last:border-0 dark:border-gray-700/30"
            >
              <div class="flex-1">
                <div class="text-sm dark:text-gray-200">{{ log.message }}</div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  {{ formatDate(log.timestamp) }}
                </div>
              </div>
              <CheckCircleIcon v-if="log.status === 'success'" class="h-5 w-5 text-green-500" />
              <XCircleIcon v-else class="h-5 w-5 text-red-500" />
            </div>
            <div
              v-if="recentLogs.length === 0"
              class="py-4 text-center text-gray-400 dark:text-gray-500"
            >
              暂无日志
            </div>
          </div>
        </Card>
      </div>
    </div>

    <div
      v-if="showUpdateModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="mx-4 w-full max-w-md rounded-lg bg-white p-6">
        <h3 class="mb-4 text-lg font-semibold">更新认证配置</h3>
        <div class="space-y-4">
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">Cookie</label>
            <textarea
              v-model="modalCookie"
              rows="3"
              class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="粘贴新的 Cookie"
            ></textarea>
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">Code</label>
            <input
              v-model="modalCode"
              type="text"
              class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="粘贴新的 Code"
            />
          </div>
        </div>
        <div class="mt-6 flex space-x-3">
          <Button @click="showUpdateModal = false" variant="secondary" class="flex-1">
            取消
          </Button>
          <Button @click="handleModalSave" :loading="saving" variant="primary" class="flex-1">
            保存
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Card from '@/components/common/Card.vue'
import Button from '@/components/common/Button.vue'
import ConfigPanel from '@/components/business/ConfigPanel.vue'
import SeatManager from '@/components/business/SeatManager.vue'
import TimePicker from '@/components/business/TimePicker.vue'
import { useConfigStore } from '@/stores/config'
import { useToast } from '@/composables/useToast'
import { logsApi } from '@/api/logs'
import { reserveApi } from '@/api/reserve'
import type { AggregatedLogEntry } from '@/types/log'
import type { Seat, DatetimeRange } from '@/types/config'
import {
  CheckCircleIcon,
  ClockIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  ClipboardDocumentListIcon,
  PlayIcon,
} from '@heroicons/vue/24/outline'

const configStore = useConfigStore()
const toast = useToast()
const config = computed(() => configStore.config)
const status = computed(() => configStore.status)

const saving = ref(false)
const running = ref(false)
const showUpdateModal = ref(false)
const modalCookie = ref('')
const modalCode = ref('')
const recentLogs = ref<AggregatedLogEntry[]>([])
const localSeats = ref<Seat[]>([])

const alertMessage = computed(() => {
  const days = config.value?.auth?.days_remaining || 0
  if (days <= 3 && days > 0) {
    return `配置将在 ${days} 天后过期`
  }
  return null
})

const statusColor = computed(() => {
  const isValid = status.value?.config_valid
  return isValid ? 'text-success' : 'text-warning'
})

const statusText = computed(() => {
  const isValid = status.value?.config_valid
  return isValid ? '正常' : '配置无效'
})

const formatNextRun = computed(() => {
  if (!status.value?.next_run) return '未设置'
  const date = new Date(status.value.next_run)
  return `${date.getMonth() + 1}/${date.getDate()} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
})

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

async function handleAuthSave(cookie: string, code: string) {
  saving.value = true
  try {
    await configStore.updateAuth(cookie, code)
    toast.success('保存成功！')
  } catch (error) {
    toast.error('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

async function handleAuthTest() {
  try {
    const response = await fetch('/api/config/test', { method: 'POST' })
    const data = await response.json()
    toast.info(data.data.message)
  } catch (error) {
    toast.error('测试失败')
  }
}

async function handleTimeSave(time: string, datetimeRange: DatetimeRange) {
  saving.value = true
  try {
    await configStore.updateReserve(time, localSeats.value, datetimeRange)
    toast.success('保存成功！')
  } catch (error) {
    toast.error('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

async function handleSeatsSave(seats: Seat[]) {
  saving.value = true
  try {
    await configStore.updateReserve(config.value?.reserve?.send_time || '07:00:02', seats)
    toast.success('保存成功！')
  } catch (error) {
    toast.error('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

async function handleModalSave() {
  await handleAuthSave(modalCookie.value, modalCode.value)
  showUpdateModal.value = false
}

async function handleRunReserve() {
  running.value = true
  try {
    const response = await reserveApi.runReserve()
    if (response.success) {
      toast.success(response.message || '执行成功')
      await loadRecentLogs()
    } else {
      toast.error(response.message || '执行失败')
    }
  } catch (error) {
    toast.error('执行失败，请检查配置')
  } finally {
    running.value = false
  }
}

async function loadRecentLogs() {
  try {
    const response = await logsApi.getLogs({ limit: 5 })
    if (response.success) {
      recentLogs.value = response.data.logs
    }
  } catch (error) {
    console.error('Failed to load logs:', error)
  }
}

onMounted(async () => {
  await configStore.fetchConfig()
  await configStore.fetchStatus()
  await loadRecentLogs()

  if (config.value?.reserve?.seats) {
    localSeats.value = [...config.value.reserve.seats]
  }
})
</script>
