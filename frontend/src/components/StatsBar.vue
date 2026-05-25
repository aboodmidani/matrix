<template>
  <div class="matrix-card px-6 py-4 mb-4">
    <div class="flex flex-wrap items-center gap-x-6 gap-y-2">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full" style="background: #00ff41; box-shadow: 0 0 6px #00ff41;"></span>
        <span class="text-xs" style="color: rgba(0,255,65,0.5);">Pass</span>
        <span class="text-sm font-bold counter-pop" style="color: #00ff41;">{{ displayPass }}</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full" style="background: #ffd700; box-shadow: 0 0 6px #ffd700;"></span>
        <span class="text-xs" style="color: rgba(0,255,65,0.5);">Scanning</span>
        <span class="text-sm font-bold counter-pop" style="color: #ffd700;">{{ displayWarn }}</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full" style="background: #ff003c; box-shadow: 0 0 6px #ff003c;"></span>
        <span class="text-xs" style="color: rgba(0,255,65,0.5);">Fail</span>
        <span class="text-sm font-bold counter-pop" style="color: #ff003c;">{{ displayFail }}</span>
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
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  stats: {
    type: Object,
    default: () => ({ pass: 0, warn: 0, fail: 0, total: 0, duration: '' }),
  },
})

const displayPass = ref(0)
const displayWarn = ref(0)
const displayFail = ref(0)

function animateValue(refVal, target, delay) {
  const steps = 20
  const stepTime = 20
  let current = 0
  const timer = setInterval(() => {
    current++
    const eased = 1 - Math.pow(1 - current / steps, 3)
    refVal.value = Math.round(eased * target)
    if (current >= steps) {
      refVal.value = target
      clearInterval(timer)
    }
  }, stepTime)
}

onMounted(() => {
  setTimeout(() => animateValue(displayPass, props.stats.pass, 0), 100)
  setTimeout(() => animateValue(displayWarn, props.stats.warn, 0), 250)
  setTimeout(() => animateValue(displayFail, props.stats.fail, 0), 400)
})
</script>
