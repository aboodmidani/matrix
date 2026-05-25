<template>
  <div class="matrix-card rounded-none overflow-hidden" :class="isRevealed ? 'hologram-in' : 'hologram-out'">
    <div class="h-px w-full" :style="{ background: 'linear-gradient(90deg, transparent, rgba(0,255,65,0.3), transparent)' }"></div>
    <div class="px-5 py-4">
      <div class="flex items-center gap-3 mb-4">
        <div class="skeleton w-6 h-6"></div>
        <div class="skeleton h-4" :style="{ width: (120 + Math.random() * 80) + 'px' }"></div>
        <div class="skeleton w-16 h-4 ml-auto"></div>
      </div>
      <div class="space-y-2.5 pl-9">
        <div class="skeleton h-3 w-full"></div>
        <div class="skeleton h-3" :style="{ width: (60 + Math.random() * 30) + '%' }"></div>
        <div class="skeleton h-3" :style="{ width: (70 + Math.random() * 25) + '%' }"></div>
      </div>
    </div>
    <div class="h-px w-full" :style="{ background: 'linear-gradient(90deg, transparent, rgba(0,255,65,0.15), transparent)' }"></div>
  </div>
</template>

<script setup>
import { useReveal } from '../composables/useReveal.js'

const { elementRef, isRevealed } = useReveal({ threshold: 0.05 })
</script>
