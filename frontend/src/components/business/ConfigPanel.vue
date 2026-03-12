<template>
  <Card>
    <template #header>
      <div class="flex items-center space-x-3">
        <LockClosedIcon class="h-6 w-6 text-primary" />
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">认证配置</h3>
      </div>
    </template>

    <div class="space-y-4">
      <div>
        <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Cookie</label
        >
        <div class="flex space-x-2">
          <input
            v-model="localCookie"
            :disabled="!editingCookie"
            type="text"
            class="glass-input flex-1 px-3 py-2 disabled:cursor-not-allowed disabled:bg-gray-100 dark:text-gray-100 dark:disabled:bg-slate-800"
            placeholder="输入 Cookie"
          />
          <Button @click="copyCookie" variant="secondary" size="md">复制</Button>
          <Button @click="toggleEditCookie" variant="secondary" size="md">
            {{ editingCookie ? '取消' : '编辑' }}
          </Button>
        </div>
      </div>

      <div>
        <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Code</label>
        <div class="flex space-x-2">
          <input
            v-model="localCode"
            :disabled="!editingCode"
            type="text"
            class="glass-input flex-1 px-3 py-2 disabled:cursor-not-allowed disabled:bg-gray-100 dark:text-gray-100 dark:disabled:bg-slate-800"
            placeholder="输入 Code"
          />
          <Button @click="copyCode" variant="secondary" size="md">复制</Button>
          <Button @click="toggleEditCode" variant="secondary" size="md">
            {{ editingCode ? '取消' : '编辑' }}
          </Button>
        </div>
      </div>

      <div class="text-sm text-gray-600 dark:text-gray-400">
        最后更新: {{ formatDate(lastUpdate) }}
        <span v-if="daysRemaining <= 3" class="ml-2 font-medium text-warning">
          (剩余 {{ daysRemaining }} 天)
        </span>
        <span v-else class="ml-2 text-gray-500 dark:text-gray-500">
          (剩余 {{ daysRemaining }} 天)
        </span>
      </div>

      <div class="flex space-x-2">
        <Button @click="handleSave" :loading="saving" variant="primary"> 保存配置 </Button>
        <Button @click="handleTest" :loading="testing" variant="secondary"> 测试配置 </Button>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Card from '../common/Card.vue'
import Button from '../common/Button.vue'
import { useToast } from '@/composables/useToast'
import { LockClosedIcon } from '@heroicons/vue/24/outline'

interface Props {
  cookie: string
  code: string
  lastUpdate: string
  daysRemaining: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  save: [cookie: string, code: string]
  test: []
}>()

const toast = useToast()
const localCookie = ref(props.cookie)
const localCode = ref(props.code)
const editingCookie = ref(false)
const editingCode = ref(false)
const saving = ref(false)
const testing = ref(false)

watch(
  () => props.cookie,
  (newVal) => {
    localCookie.value = newVal
  }
)

watch(
  () => props.code,
  (newVal) => {
    localCode.value = newVal
  }
)

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleString('zh-CN')
}

async function copyCookie() {
  try {
    await navigator.clipboard.writeText(localCookie.value)
    toast.success('Cookie 已复制到剪贴板！')
  } catch (error) {
    toast.error('复制失败，请手动复制')
  }
}

async function copyCode() {
  try {
    await navigator.clipboard.writeText(localCode.value)
    toast.success('Code 已复制到剪贴板！')
  } catch (error) {
    toast.error('复制失败，请手动复制')
  }
}

function toggleEditCookie() {
  if (!editingCookie.value) {
    editingCookie.value = true
  } else {
    localCookie.value = props.cookie
    editingCookie.value = false
  }
}

function toggleEditCode() {
  if (!editingCode.value) {
    editingCode.value = true
  } else {
    localCode.value = props.code
    editingCode.value = false
  }
}

async function handleSave() {
  saving.value = true
  try {
    emit('save', localCookie.value, localCode.value)
  } finally {
    saving.value = false
  }
}

async function handleTest() {
  testing.value = true
  try {
    emit('test')
  } finally {
    testing.value = false
  }
}
</script>
