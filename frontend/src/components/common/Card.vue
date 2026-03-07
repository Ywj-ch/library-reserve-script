<template>
  <div class="rounded-lg border border-gray-200 bg-white shadow-sm">
    <div v-if="title" class="border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
        <slot name="actions" />
      </div>
    </div>
    <div class="px-6 py-4">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
}

defineProps<Props>()
</script>
