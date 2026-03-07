<template>
  <div class="space-y-6">
    <Card title="📊 统计概览">
      <div class="grid grid-cols-2 gap-4 md:grid-cols-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-gray-900">{{ stats?.total_requests || 0 }}</div>
          <div class="text-sm text-gray-600">总请求数</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-success">{{ stats?.success_count || 0 }}</div>
          <div class="text-sm text-gray-600">成功次数</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-error">{{ stats?.failure_count || 0 }}</div>
          <div class="text-sm text-gray-600">失败次数</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-primary">{{ stats?.success_rate || 0 }}%</div>
          <div class="text-sm text-gray-600">成功率</div>
        </div>
      </div>
    </Card>

    <Card title="🔍 筛选">
      <div class="flex flex-wrap gap-4">
        <div class="min-w-[200px] flex-1">
          <label class="mb-2 block text-sm font-medium text-gray-700">日期</label>
          <input
            v-model="filters.date"
            type="date"
            class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        <div class="min-w-[200px] flex-1">
          <label class="mb-2 block text-sm font-medium text-gray-700">状态</label>
          <select
            v-model="filters.status"
            class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="">全部</option>
            <option value="success">成功</option>
            <option value="failure">失败</option>
          </select>
        </div>
        <div class="flex items-end">
          <Button @click="loadLogs" variant="primary">搜索</Button>
        </div>
      </div>
    </Card>

    <Card title="📝 日志记录">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-600">时间</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-600">状态</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-600">座位</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-600">消息</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="log in logs"
              :key="log.timestamp"
              class="border-b border-gray-100 hover:bg-gray-50"
            >
              <td class="px-4 py-3 text-sm text-gray-900">
                {{ formatDate(log.timestamp) }}
              </td>
              <td class="px-4 py-3 text-sm">
                <span
                  :class="log.status === 'success' ? 'text-success' : 'text-error'"
                  class="font-medium"
                >
                  {{ log.status === 'success' ? '✅ 成功' : '❌ 失败' }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-600">
                {{ log.seat || '-' }}
              </td>
              <td class="px-4 py-3 text-sm text-gray-900">
                {{ log.message }}
              </td>
            </tr>
            <tr v-if="logs.length === 0">
              <td colspan="4" class="px-4 py-8 text-center text-gray-400">暂无日志记录</td>
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
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Card from '@/components/common/Card.vue'
import Button from '@/components/common/Button.vue'
import { logsApi } from '@/api/logs'
import type { LogEntry, LogStats, LogPagination } from '@/types/log'

const logs = ref<LogEntry[]>([])
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

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleString('zh-CN')
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
