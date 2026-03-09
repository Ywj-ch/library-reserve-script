<template>
  <div class="min-h-screen pt-24 pb-8 px-4">
    <div class="max-w-7xl mx-auto space-y-6">
      <Card>
        <template #header>
          <div class="flex items-center space-x-3">
            <ChartBarIcon class="w-6 h-6 text-primary" />
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">统计概览</h3>
          </div>
        </template>
        <div class="grid grid-cols-2 gap-6 md:grid-cols-4">
          <div class="text-center">
            <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ stats?.total_requests || 0 }}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">总请求数</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-green-600">{{ stats?.success_count || 0 }}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">成功次数</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-red-600">{{ stats?.failure_count || 0 }}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">失败次数</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-primary">{{ stats?.success_rate || 0 }}%</div>
            <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">成功率</div>
          </div>
        </div>
      </Card>

      <Card>
        <template #header>
          <div class="flex items-center space-x-3">
            <FunnelIcon class="w-6 h-6 text-primary" />
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">筛选</h3>
          </div>
        </template>
        <div class="flex flex-wrap gap-4">
          <div class="min-w-[200px] flex-1">
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">日期</label>
            <div class="relative">
              <input
                v-model="filters.date"
                type="date"
                :max="today"
                class="glass-input w-full px-3 py-2 pr-10 cursor-pointer dark:text-gray-100"
              />
              <CalendarIcon class="w-5 h-5 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>
          </div>
          <div class="min-w-[200px] flex-1">
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">状态</label>
            <select
              v-model="filters.status"
              class="glass-input w-full px-3 py-2 dark:text-gray-100"
            >
              <option value="">全部</option>
              <option value="success">成功</option>
              <option value="failure">失败</option>
            </select>
          </div>
          <div class="flex items-end">
            <Button @click="loadLogs" variant="primary">
              <MagnifyingGlassIcon class="w-4 h-4 mr-2" />
              搜索
            </Button>
          </div>
        </div>
      </Card>

      <Card>
        <template #header>
          <div class="flex items-center space-x-3">
            <DocumentTextIcon class="w-6 h-6 text-primary" />
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">预约记录</h3>
          </div>
        </template>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-700/50">
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700 dark:text-gray-300 w-12"></th>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700 dark:text-gray-300">时间</th>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700 dark:text-gray-300">状态</th>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700 dark:text-gray-300">尝试次数</th>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700 dark:text-gray-300">结果摘要</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="log in logs" :key="log.session_id">
                <tr
                  class="border-b border-gray-100 dark:border-gray-700/30 hover:bg-white/50 dark:hover:bg-white/5 transition-colors cursor-pointer"
                  @click="toggleExpand(log.session_id)"
                >
                  <td class="px-4 py-3">
                    <ChevronDownIcon 
                      class="w-5 h-5 text-gray-400 transition-transform duration-200"
                      :class="{ 'rotate-180': expandedSessions.has(log.session_id) }"
                    />
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-900 dark:text-gray-100">
                    {{ formatDate(log.timestamp) }}
                  </td>
                  <td class="px-4 py-3 text-sm">
                    <div class="flex items-center space-x-2">
                      <CheckCircleIcon v-if="log.status === 'success'" class="w-5 h-5 text-green-600" />
                      <XCircleIcon v-else class="w-5 h-5 text-red-600" />
                      <span
                        :class="log.status === 'success' ? 'text-green-600' : 'text-red-600'"
                        class="font-medium"
                      >
                        {{ log.status === 'success' ? '成功' : '失败' }}
                      </span>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                    {{ log.total_attempts }} 次
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-900 dark:text-gray-100">
                    {{ log.message }}
                  </td>
                </tr>
                <tr v-if="expandedSessions.has(log.session_id)" class="bg-gray-50 dark:bg-slate-900">
                  <td colspan="5" class="px-4 py-4">
                    <div class="space-y-4">
                      <div>
                        <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 flex items-center">
                          <CubeIcon class="w-4 h-4 mr-2" />
                          座位尝试详情
                        </h4>
                        <div class="grid gap-2">
                          <div
                            v-for="(seat, idx) in log.seats"
                            :key="idx"
                            class="flex items-center justify-between p-3 bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700"
                          >
                            <div class="flex items-center space-x-3">
                              <span class="font-mono text-sm font-medium text-gray-900 dark:text-gray-100">{{ seat.seat_id }}</span>
                              <span class="text-xs text-gray-500 dark:text-gray-400">HTTP {{ seat.status_code }}</span>
                            </div>
                            <div class="flex items-center space-x-2">
                              <CheckCircleIcon v-if="seat.success" class="w-4 h-4 text-green-600" />
                              <XCircleIcon v-else class="w-4 h-4 text-red-600" />
                              <span :class="seat.success ? 'text-green-600' : 'text-red-600'" class="text-sm">
                                {{ seat.success ? '成功' : '失败' }}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div>
                        <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 flex items-center">
                          <DocumentTextIcon class="w-4 h-4 mr-2" />
                          执行日志
                        </h4>
                        <div class="bg-gray-900/90 rounded-lg p-4 font-mono text-xs text-gray-300 max-h-64 overflow-y-auto">
                          <div v-for="(detail, idx) in log.details" :key="idx" class="py-0.5">
                            {{ detail }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </td>
                </tr>
              </template>
              <tr v-if="logs.length === 0">
                <td colspan="5" class="px-4 py-8 text-center text-gray-400 dark:text-gray-500">暂无日志记录</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div
          v-if="pagination.total > 0"
          class="mt-4 flex items-center justify-between border-t border-gray-200 pt-4"
        >
          <div class="text-sm text-gray-600">共 {{ pagination.total }} 条记录</div>
          <div class="flex space-x-2">
            <Button
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
              variant="secondary"
              size="sm"
            >
              上一页
            </Button>
            <span class="px-4 py-2 text-sm text-gray-700">
              {{ currentPage }} / {{ totalPages }}
            </span>
            <Button
              @click="changePage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              variant="secondary"
              size="sm"
            >
              下一页
            </Button>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Card from '@/components/common/Card.vue'
import Button from '@/components/common/Button.vue'
import { logsApi } from '@/api/logs'
import type { AggregatedLogEntry, LogStats, LogPagination } from '@/types/log'
import {
  ChartBarIcon,
  FunnelIcon,
  DocumentTextIcon,
  CheckCircleIcon,
  XCircleIcon,
  MagnifyingGlassIcon,
  ChevronDownIcon,
  CubeIcon,
  CalendarIcon,
} from '@heroicons/vue/24/outline'

const logs = ref<AggregatedLogEntry[]>([])
const stats = ref<LogStats | null>(null)
const pagination = ref<LogPagination>({
  total: 0,
  page: 1,
  limit: 20,
})

const filters = ref({
  date: '',
  status: '',
})

const currentPage = ref(1)
const totalPages = computed(() => Math.ceil(pagination.value.total / pagination.value.limit))
const expandedSessions = ref(new Set<string>())

const today = computed(() => {
  const date = new Date()
  return date.toISOString().split('T')[0]
})

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleString('zh-CN')
}

function toggleExpand(sessionId: string) {
  if (expandedSessions.value.has(sessionId)) {
    expandedSessions.value.delete(sessionId)
  } else {
    expandedSessions.value.add(sessionId)
  }
}

async function loadLogs() {
  try {
    const response = await logsApi.getLogs({
      page: currentPage.value,
      limit: pagination.value.limit,
      date: filters.value.date || undefined,
      status: filters.value.status || undefined,
    })

    if (response.success) {
      logs.value = response.data.logs
      pagination.value = response.data.pagination
    }
  } catch (error) {
    console.error('Failed to load logs:', error)
  }
}

async function loadStats() {
  try {
    const response = await logsApi.getStats()
    if (response.success) {
      stats.value = response.data
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

function changePage(page: number) {
  currentPage.value = page
  loadLogs()
}

onMounted(() => {
  loadLogs()
  loadStats()
})
</script>
