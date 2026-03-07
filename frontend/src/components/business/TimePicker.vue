<template>
  <Card title="⏰ 发送时间">
    <div class="space-y-4">
      <div class="flex items-center space-x-2">
        <div class="flex-1">
          <label class="mb-2 block text-sm font-medium text-gray-700">预约时间</label>
          <div class="flex items-center space-x-2">
            <input
              v-model.number="hours"
              type="number"
              min="0"
              max="23"
              class="w-20 rounded-md border border-gray-300 px-3 py-2 text-center focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <span class="text-lg font-medium">:</span>
            <input
              v-model.number="minutes"
              type="number"
              min="0"
              max="59"
              class="w-20 rounded-md border border-gray-300 px-3 py-2 text-center focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <span class="text-lg font-medium">:</span>
            <input
              v-model.number="seconds"
              type="number"
              min="0"
              max="59"
              class="w-20 rounded-md border border-gray-300 px-3 py-2 text-center focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>
      </div>

      <div class="text-sm text-gray-600">下次预约时间: {{ formatTime(nextRun) }}</div>

      <Button @click="handleSave" :loading="saving" variant="primary" class="w-full">
        保存时间设置
      </Button>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import Card from '../common/Card.vue'
import Button from '../common/Button.vue'

interface Props {
  sendTime: string
  nextRun?: string
  saving?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  saving: false,
})

const emit = defineEmits<{
  save: [time: string]
}>()

const timeParts = props.sendTime.split(':').map(Number)
const hours = ref(timeParts[0] || 7)
const minutes = ref(timeParts[1] || 0)
const seconds = ref(timeParts[2] || 2)

watch(
  () => props.sendTime,
  (newVal) => {
    const parts = newVal.split(':').map(Number)
    hours.value = parts[0] || 7
    minutes.value = parts[1] || 0
    seconds.value = parts[2] || 2
  }
)

const formattedTime = computed(() => {
  const h = String(hours.value).padStart(2, '0')
  const m = String(minutes.value).padStart(2, '0')
  const s = String(seconds.value).padStart(2, '0')
  return `${h}:${m}:${s}`
})

function formatTime(dateString?: string): string {
  if (!dateString) return '未设置'
  return new Date(dateString).toLocaleString('zh-CN')
}

function handleSave() {
  emit('save', formattedTime.value)
}
</script>
