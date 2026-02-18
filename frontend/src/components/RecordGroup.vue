<template>
  <div v-if="items && items.length">
    <p class="text-green-600 text-xs mb-1">{{ label }}</p>
    <div class="flex flex-wrap gap-2 mb-2">
      <span
        v-for="item in items"
        :key="item"
        class="text-sm text-blue-300 bg-blue-900/20 border border-blue-800/40 rounded px-2 py-0.5"
      >
        {{ item }}
      </span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  items: { type: Array, default: () => [] },
})
</script>
