<template>
  <Card>
    <template #header>
      <div class="flex items-center space-x-3">
        <ClockIcon class="h-6 w-6 text-primary" />
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">发送时间</h3>
      </div>
    </template>

    <div class="space-y-4">
      <div class="flex items-center space-x-2">
        <div class="flex-1">
          <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300"
            >预约时间</label
          >
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

      <div class="border-t border-gray-200 pt-4 dark:border-gray-700">
        <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300"
          >预约时间段</label
        >
        <div class="mb-2 flex items-center space-x-2">
          <input
            :value="String(startHours).padStart(2, '0')"
            @input="startHours = Number(($event.target as HTMLInputElement).value)"
            type="number"
            min="0"
            max="23"
            class="glass-input w-16 px-2 py-1.5 text-center text-base font-medium dark:text-gray-100"
          />
          <span class="text-lg font-bold text-gray-400">:</span>
          <input
            :value="String(startMinutes).padStart(2, '0')"
            @input="startMinutes = Number(($event.target as HTMLInputElement).value)"
            type="number"
            min="0"
            max="59"
            class="glass-input w-16 px-2 py-1.5 text-center text-base font-medium dark:text-gray-100"
          />
          <span class="mx-2 text-lg font-medium text-gray-500">至</span>
          <input
            :value="String(endHours).padStart(2, '0')"
            @input="endHours = Number(($event.target as HTMLInputElement).value)"
            type="number"
            min="0"
            max="23"
            class="glass-input w-16 px-2 py-1.5 text-center text-base font-medium dark:text-gray-100"
          />
          <span class="text-lg font-bold text-gray-400">:</span>
          <input
            :value="String(endMinutes).padStart(2, '0')"
            @input="endMinutes = Number(($event.target as HTMLInputElement).value)"
            type="number"
            min="0"
            max="59"
            class="glass-input w-16 px-2 py-1.5 text-center text-base font-medium dark:text-gray-100"
          />
        </div>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="preset in presets"
            :key="preset.value"
            @click="applyPreset(preset.value)"
            class="rounded-full border border-gray-300 px-3 py-1 text-xs text-gray-700 transition-colors hover:bg-gray-100 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
          >
            {{ preset.label }}
          </button>
        </div>
      </div>

      <div
        class="rounded-lg border border-blue-200/50 bg-gradient-to-r from-blue-50 to-indigo-50 p-4 dark:border-slate-600 dark:from-slate-800 dark:to-slate-700"
      >
        <div class="mb-2 flex items-center space-x-2">
          <InformationCircleIcon class="h-5 w-5 text-blue-600 dark:text-blue-400" />
          <div class="font-semibold text-blue-900 dark:text-blue-200">当前设置</div>
        </div>
        <div class="mb-1 text-2xl font-bold text-blue-900 dark:text-blue-100">
          {{ formattedTime }}
        </div>
        <div class="mb-3 text-sm text-blue-700 dark:text-blue-300">
          预约时段: {{ formattedDatetimeRange }}
        </div>
        <div class="flex items-center space-x-2 text-sm">
          <CalendarIcon class="h-4 w-4 text-blue-700 dark:text-blue-300" />
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
import type { DatetimeRange } from '@/types/config'

interface Props {
  sendTime: string
  datetimeRange?: DatetimeRange
  nextRun?: string
  saving?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  saving: false,
})

const emit = defineEmits<{
  save: [time: string, datetimeRange: DatetimeRange]
}>()

const timeParts = props.sendTime.split(':').map(Number)
const hours = ref(timeParts[0] || 7)
const minutes = ref(timeParts[1] || 0)
const seconds = ref(timeParts[2] || 2)

const startHours = ref(11)
const startMinutes = ref(0)
const endHours = ref(22)
const endMinutes = ref(30)

const presets = [
  { label: '8点', value: '08:00' },
  { label: '11点', value: '11:00' },
  { label: '13点', value: '13:00' },
  { label: '17点', value: '17:00' },
]

watch(
  () => props.sendTime,
  (newVal) => {
    const parts = newVal.split(':').map(Number)
    hours.value = parts[0] || 7
    minutes.value = parts[1] || 0
    seconds.value = parts[2] || 2
  }
)

watch(
  () => props.datetimeRange,
  (newVal) => {
    if (newVal) {
      const [sh, sm] = newVal.start.split(':').map(Number)
      const [eh, em] = newVal.end.split(':').map(Number)
      startHours.value = sh || 11
      startMinutes.value = sm || 0
      endHours.value = eh || 22
      endMinutes.value = em || 30
    }
  },
  { immediate: true }
)

const formattedTime = computed(() => {
  const h = String(hours.value).padStart(2, '0')
  const m = String(minutes.value).padStart(2, '0')
  const s = String(seconds.value).padStart(2, '0')
  return `${h}:${m}:${s}`
})

const formattedDatetimeRange = computed(() => {
  const sh = String(startHours.value).padStart(2, '0')
  const sm = String(startMinutes.value).padStart(2, '0')
  const eh = String(endHours.value).padStart(2, '0')
  const em = String(endMinutes.value).padStart(2, '0')
  return `${sh}:${sm} - ${eh}:${em}`
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

function applyPreset(value: string) {
  const [h, m] = value.split(':').map(Number)
  startHours.value = h
  startMinutes.value = m
}

function handleSave() {
  const sh = String(startHours.value).padStart(2, '0')
  const sm = String(startMinutes.value).padStart(2, '0')
  const eh = String(endHours.value).padStart(2, '0')
  const em = String(endMinutes.value).padStart(2, '0')

  emit('save', formattedTime.value, {
    start: `${sh}:${sm}`,
    end: `${eh}:${em}`,
  })
}
</script>
