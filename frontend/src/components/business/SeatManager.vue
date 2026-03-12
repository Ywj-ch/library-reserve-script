<template>
  <Card>
    <template #header>
      <div class="flex items-center space-x-3">
        <BuildingOffice2Icon class="h-6 w-6 text-primary" />
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">座位列表</h3>
      </div>
    </template>

    <div class="space-y-3">
      <div
        v-for="(seat, index) in modelValue"
        :key="seat.id"
        class="glass-card flex items-center justify-between p-4"
      >
        <div class="flex items-center space-x-3">
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ index + 1 }}.</span>
          <span class="font-semibold text-gray-900 dark:text-gray-100">{{ seat.id }}</span>
          <span class="text-sm text-gray-600 dark:text-gray-400">({{ seat.name }})</span>
          <span
            :class="seat.enabled ? 'text-green-600' : 'text-red-500'"
            class="flex items-center space-x-1 text-xs font-medium"
          >
            <CheckCircleIcon v-if="seat.enabled" class="h-4 w-4" />
            <XCircleIcon v-else class="h-4 w-4" />
            <span>{{ seat.enabled ? '启用' : '禁用' }}</span>
          </span>
        </div>
        <div class="flex space-x-1">
          <button
            @click="moveUp(index)"
            :disabled="index === 0"
            class="rounded-lg p-2 text-gray-600 transition-all hover:bg-white/50 hover:text-primary disabled:cursor-not-allowed disabled:opacity-50 dark:text-gray-400 dark:hover:bg-white/10"
          >
            <ArrowUpIcon class="h-4 w-4" />
          </button>
          <button
            @click="moveDown(index)"
            :disabled="index === modelValue.length - 1"
            class="rounded-lg p-2 text-gray-600 transition-all hover:bg-white/50 hover:text-primary disabled:cursor-not-allowed disabled:opacity-50 dark:text-gray-400 dark:hover:bg-white/10"
          >
            <ArrowDownIcon class="h-4 w-4" />
          </button>
          <button
            @click="toggleSeat(index)"
            class="rounded-lg p-2 text-gray-600 transition-all hover:bg-white/50 hover:text-warning dark:text-gray-400 dark:hover:bg-white/10"
          >
            <PowerIcon class="h-4 w-4" />
          </button>
          <button
            @click="removeSeat(index)"
            class="rounded-lg p-2 text-gray-600 transition-all hover:bg-white/50 hover:text-error dark:text-gray-400 dark:hover:bg-white/10"
          >
            <TrashIcon class="h-4 w-4" />
          </button>
        </div>
      </div>

      <div class="flex space-x-2">
        <input
          v-model="newSeatId"
          type="text"
          placeholder="座位ID (如: Z41N001)"
          class="glass-input flex-1 px-3 py-2 dark:text-gray-100"
          @keyup.enter="addSeat"
        />
        <Button @click="addSeat" variant="primary" size="md"> 添加 </Button>
      </div>

      <Button @click="handleSave" :loading="saving" variant="primary" class="w-full">
        保存座位列表
      </Button>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Card from '../common/Card.vue'
import Button from '../common/Button.vue'
import {
  BuildingOffice2Icon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  PowerIcon,
  TrashIcon,
} from '@heroicons/vue/24/outline'
import type { Seat } from '@/types/config'
import { useToast } from '@/composables/useToast'

interface Props {
  modelValue: Seat[]
  saving?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  saving: false,
})

const emit = defineEmits<{
  'update:modelValue': [seats: Seat[]]
  save: [seats: Seat[]]
}>()

const toast = useToast()
const newSeatId = ref('')

function moveUp(index: number) {
  if (index > 0) {
    const newSeats = [...props.modelValue]
    ;[newSeats[index - 1], newSeats[index]] = [newSeats[index], newSeats[index - 1]]
    emit('update:modelValue', newSeats)
    toast.success(`${newSeats[index - 1].id} 已上移`)
  }
}

function moveDown(index: number) {
  if (index < props.modelValue.length - 1) {
    const newSeats = [...props.modelValue]
    ;[newSeats[index], newSeats[index + 1]] = [newSeats[index + 1], newSeats[index]]
    emit('update:modelValue', newSeats)
    toast.success(`${newSeats[index + 1].id} 已下移`)
  }
}

function toggleSeat(index: number) {
  const newSeats = [...props.modelValue]
  newSeats[index] = { ...newSeats[index], enabled: !newSeats[index].enabled }
  emit('update:modelValue', newSeats)
  const action = newSeats[index].enabled ? '启用' : '禁用'
  toast.info(`${newSeats[index].id} 已${action}`)
}

function removeSeat(index: number) {
  if (confirm('确定要删除这个座位吗？')) {
    const seatId = props.modelValue[index].id
    const newSeats = props.modelValue.filter((_, i) => i !== index)
    emit('update:modelValue', newSeats)
    toast.success(`${seatId} 已删除`)
  }
}

function addSeat() {
  if (newSeatId.value.trim()) {
    const newSeat: Seat = {
      id: newSeatId.value.trim(),
      name: newSeatId.value.trim().slice(-3),
      enabled: true,
    }
    emit('update:modelValue', [...props.modelValue, newSeat])
    toast.success(`${newSeat.id} 已添加`)
    newSeatId.value = ''
  }
}

function handleSave() {
  emit('save', props.modelValue)
}
</script>
