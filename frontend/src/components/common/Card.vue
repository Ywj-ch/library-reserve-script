<template>
  <div class="glass-card rounded-2xl">
    <div v-if="hasHeader" class="border-b border-white/20 px-6 py-4 dark:border-gray-700/30">
      <div class="flex items-center justify-between">
        <div>
          <slot name="header">
            <h3 v-if="title" class="text-lg font-semibold text-gray-800 dark:text-gray-100">
              {{ title }}
            </h3>
          </slot>
        </div>
        <slot name="actions" />
      </div>
    </div>
    <div class="px-6 py-4">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, useSlots } from 'vue'

interface Props {
  title?: string
}

const props = defineProps<Props>()
const slots = useSlots()

const hasHeader = computed(() => {
  return props.title || slots.header || slots.actions
})
</script>
