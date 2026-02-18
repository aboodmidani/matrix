<template>
  <div class="bg-black/90 border rounded-lg overflow-hidden" :class="`border-${config.color}-500/40`">
    <!-- Header -->
    <button
      @click="open = !open"
      class="w-full px-5 py-4 flex items-center justify-between transition-colors"
      :class="`hover:bg-${config.color}-900/10`"
    >
      <div class="flex items-center gap-3">
        <span class="text-xl">{{ config.icon }}</span>
        <span class="font-bold" :class="`text-${config.color}-400`">{{ config.label }}</span>
        <span v-if="scan.status === 'scanning'" class="text-xs text-yellow-400 animate-pulse">[SCANNING…]</span>
        <span v-else-if="scan.status === 'done'"  class="text-xs text-green-400">[DONE]</span>
        <span v-else-if="scan.status === 'error'" class="text-xs text-red-400">[ERROR]</span>
      </div>
      <svg
        class="w-4 h-4 transition-transform"
        :class="[open ? 'rotate-180' : '', `text-${config.color}-500`]"
        fill="none" stroke="currentColor" viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Body -->
    <div v-if="open" class="px-5 pb-5 border-t" :class="`border-${config.color}-900/40`">
      <div v-if="scan.status === 'scanning'" class="mt-4 text-yellow-400 text-sm animate-pulse">
        Running scan…
      </div>
      <div v-else-if="scan.status === 'error'" class="mt-4 text-red-400 text-sm">
        ✗ {{ scan.error }}
      </div>
      <div v-else-if="scan.status === 'done' && scan.data" class="mt-4">
        <slot name="results" :data="scan.data" />
      </div>
      <div v-else class="mt-4 text-green-800 text-sm">No data.</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  config: { type: Object, required: true },
  scan:   { type: Object, required: true },
})

const open = ref(true)
</script>
