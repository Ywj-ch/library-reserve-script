<template>
  <Card title="🔐 认证配置">
    <div class="space-y-4">
      <div>
        <label class="mb-2 block text-sm font-medium text-gray-700">Cookie</label>
        <div class="flex space-x-2">
          <input
            v-model="localCookie"
            type="text"
            class="flex-1 rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="输入 Cookie"
          />
          <Button @click="copyCookie" variant="secondary" size="md">复制</Button>
          <Button @click="toggleEditCookie" variant="secondary" size="md">
            {{ editingCookie ? '取消' : '编辑' }}
          </Button>
        </div>
      </div>

      <div>
        <label class="mb-2 block text-sm font-medium text-gray-700">Code</label>
        <div class="flex space-x-2">
          <input
            v-model="localCode"
            type="text"
            class="flex-1 rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="输入 Code"
          />
          <Button @click="copyCode" variant="secondary" size="md">复制</Button>
          <Button @click="toggleEditCode" variant="secondary" size="md">
            {{ editingCode ? '取消' : '编辑' }}
          </Button>
        </div>
      </div>

      <div class="text-sm text-gray-600">
        最后更新: {{ formatDate(lastUpdate) }}
        <span v-if="daysRemaining <= 3" class="ml-2 font-medium text-warning">
          (剩余 {{ daysRemaining }} 天)
        </span>
        <span v-else class="ml-2 text-gray-500"> (剩余 {{ daysRemaining }} 天) </span>
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

function copyCookie() {
  navigator.clipboard.writeText(localCookie.value)
}

function copyCode() {
  navigator.clipboard.writeText(localCode.value)
}

function toggleEditCookie() {
  editingCookie.value = !editingCookie.value
}

function toggleEditCode() {
  editingCode.value = !editingCode.value
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
