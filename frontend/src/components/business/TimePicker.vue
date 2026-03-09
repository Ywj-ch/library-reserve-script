<template>
  <Card>
    <template #header>
      <div class="flex items-center space-x-3">
        <ClockIcon class="w-6 h-6 text-primary" />
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">发送时间</h3>
      </div>
    </template>

    <div class="space-y-4">
      <div class="flex items-center space-x-2">
        <div class="flex-1">
          <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">预约时间</label>
          <div class="flex items-center space-x-2">
            <input
              :value="String(hours).padStart(2, '0')"
              @input="hours = Number(($event.target as HTMLInputElement).value)"
              type="number"
              min="0"
              max="23"
              class="glass-input w-20 px-3 py-2 text-center text-lg font-medium dark:text-gray-100"
            />
            <span class="text-2xl font-bold text-gray-400">:</span>
            <input
              :value="String(minutes).padStart(2, '0')"
              @input="minutes = Number(($event.target as HTMLInputElement).value)"
              type="number"
              min="0"
              max="59"
              class="glass-input w-20 px-3 py-2 text-center text-lg font-medium dark:text-gray-100"
            />
            <span class="text-2xl font-bold text-gray-400">:</span>
            <input
              :value="String(seconds).padStart(2, '0')"
              @input="seconds = Number(($event.target as HTMLInputElement).value)"
              type="number"
              min="0"
              max="59"
              class="glass-input w-20 px-3 py-2 text-center text-lg font-medium dark:text-gray-100"
            />
          </div>
        </div>
      </div>

      <div class="rounded-lg bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-slate-800 dark:to-slate-700 border border-blue-200/50 dark:border-slate-600 p-4">
        <div class="flex items-center space-x-2 mb-2">
          <InformationCircleIcon class="w-5 h-5 text-blue-600 dark:text-blue-400" />
          <div class="font-semibold text-blue-900 dark:text-blue-200">当前设置</div>
        </div>
        <div class="text-2xl font-bold text-blue-900 dark:text-blue-100 mb-3">{{ formattedTime }}</div>
        <div class="flex items-center space-x-2 text-sm">
          <CalendarIcon class="w-4 h-4 text-blue-700 dark:text-blue-300" />
          <div class="text-blue-700 dark:text-blue-300">下次预约时间: {{ formatNextRun }}</div>
        </div>
      </div>

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
import { ClockIcon, InformationCircleIcon, CalendarIcon } from '@heroicons/vue/24/outline'

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

const formatNextRun = computed(() => {
  if (!props.nextRun) return '未设置'

  const nextRunDate = new Date(props.nextRun)
  const [h, m, s] = formattedTime.value.split(':').map(Number)

  nextRunDate.setHours(h, m, s)

  return nextRunDate.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
})

function handleSave() {
  emit('save', formattedTime.value)
}
</script>
