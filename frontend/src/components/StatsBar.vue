<template>
  <div
    ref="barRef"
    class="matrix-card px-6 py-4 mb-4"
    :class="isRevealed ? 'hologram-in' : 'hologram-out'"
  >
    <div class="flex flex-wrap items-center gap-x-6 gap-y-2">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full" style="background: #00ff41; box-shadow: 0 0 6px #00ff41;"></span>
        <span class="text-xs" style="color: rgba(0,255,65,0.5);">Pass</span>
        <span class="text-sm font-bold" style="color: #00ff41;">{{ stats.pass }}</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full" style="background: #ffd700; box-shadow: 0 0 6px #ffd700;"></span>
        <span class="text-xs" style="color: rgba(0,255,65,0.5);">Warn</span>
        <span class="text-sm font-bold" style="color: #ffd700;">{{ stats.warn }}</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full" style="background: #ff003c; box-shadow: 0 0 6px #ff003c;"></span>
        <span class="text-xs" style="color: rgba(0,255,65,0.5);">Fail</span>
        <span class="text-sm font-bold" style="color: #ff003c;">{{ stats.fail }}</span>
      </div>
      <div class="h-4 w-px" style="background: rgba(0,255,65,0.15);"></div>
      <div class="flex items-center gap-2">
        <span class="text-xs" style="color: rgba(0,255,65,0.5);">Scanned</span>
        <span class="text-sm font-bold" style="color: #00ff41;">{{ stats.total }} checks</span>
      </div>
      <div v-if="stats.duration" class="flex items-center gap-2">
        <span class="text-xs" style="color: rgba(0,255,65,0.5);">Duration</span>
        <span class="text-sm font-bold" style="color: #00ff41;">{{ stats.duration }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useReveal } from '../composables/useReveal.js'

defineProps({
  stats: {
    type: Object,
    default: () => ({ pass: 0, warn: 0, fail: 0, total: 0, duration: '' }),
  },
})

const { elementRef: barRef, isRevealed } = useReveal({ threshold: 0.1 })
</script>
