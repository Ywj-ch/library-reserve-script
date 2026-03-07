<template>
  <Card title="💺 座位列表">
    <div class="space-y-3">
      <div
        v-for="(seat, index) in modelValue"
        :key="seat.id"
        class="flex items-center justify-between rounded-md bg-gray-50 p-3"
      >
        <div class="flex items-center space-x-3">
          <span class="text-sm text-gray-500">{{ index + 1 }}.</span>
          <span class="font-medium">{{ seat.id }}</span>
          <span class="text-sm text-gray-600">({{ seat.name }})</span>
          <span :class="seat.enabled ? 'text-success' : 'text-gray-400'" class="text-xs">
            {{ seat.enabled ? '✅ 启用' : '❌ 禁用' }}
          </span>
        </div>
        <div class="flex space-x-1">
          <button
            @click="moveUp(index)"
            :disabled="index === 0"
            class="p-1 text-gray-600 hover:text-primary disabled:cursor-not-allowed disabled:opacity-50"
          >
            ⬆️
          </button>
          <button
            @click="moveDown(index)"
            :disabled="index === modelValue.length - 1"
            class="p-1 text-gray-600 hover:text-primary disabled:cursor-not-allowed disabled:opacity-50"
          >
            ⬇️
          </button>
          <button @click="toggleSeat(index)" class="p-1 text-gray-600 hover:text-warning">
            {{ seat.enabled ? '🔇' : '🔊' }}
          </button>
          <button @click="removeSeat(index)" class="p-1 text-gray-600 hover:text-error">🗑️</button>
        </div>
      </div>

      <div class="flex space-x-2">
        <input
          v-model="newSeatId"
          type="text"
          placeholder="座位ID (如: Z41N001)"
          class="flex-1 rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary"
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
import type { Seat } from '@/types/config'

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

const newSeatId = ref('')

function moveUp(index: number) {
  if (index > 0) {
    const newSeats = [...props.modelValue]
    ;[newSeats[index - 1], newSeats[index]] = [newSeats[index], newSeats[index - 1]]
    emit('update:modelValue', newSeats)
  }
}

function moveDown(index: number) {
  if (index < props.modelValue.length - 1) {
    const newSeats = [...props.modelValue]
    ;[newSeats[index], newSeats[index + 1]] = [newSeats[index + 1], newSeats[index]]
    emit('update:modelValue', newSeats)
  }
}

function toggleSeat(index: number) {
  const newSeats = [...props.modelValue]
  newSeats[index] = { ...newSeats[index], enabled: !newSeats[index].enabled }
  emit('update:modelValue', newSeats)
}

function removeSeat(index: number) {
  if (confirm('确定要删除这个座位吗？')) {
    const newSeats = props.modelValue.filter((_, i) => i !== index)
    emit('update:modelValue', newSeats)
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
    newSeatId.value = ''
  }
}

function handleSave() {
  emit('save', props.modelValue)
}
</script>
