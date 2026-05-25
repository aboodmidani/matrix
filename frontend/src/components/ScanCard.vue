<template>
  <div class="matrix-card rounded-none fade-in-up" :style="cardStyle">
    <div class="h-px w-full" :style="{ background: `linear-gradient(90deg, transparent, ${accentColor}, transparent)` }"></div>

    <button
      @click="open = !open"
      class="w-full px-5 py-4 flex items-center justify-between group transition-all duration-200"
      :style="open ? { background: `rgba(${accentRgb}, 0.05)` } : {}"
    >
      <div class="flex items-center gap-3 min-w-0">
        <span class="text-lg flex-shrink-0">{{ config.icon }}</span>
        <span class="font-bold tracking-wider text-sm uppercase" :style="{ color: accentColor, fontFamily: 'Orbitron, monospace' }">
          {{ config.label }}
        </span>
        <span v-if="scan.status === 'scanning'" class="badge-scanning flex-shrink-0">
          <span class="inline-block w-1.5 h-1.5 rounded-full bg-yellow-400 animate-ping"></span>
          SCANNING
        </span>
        <span v-else-if="scan.status === 'done'" class="badge-done flex-shrink-0">
          &#10003; DONE
        </span>
        <span v-else-if="scan.status === 'error'" class="badge-error flex-shrink-0">
          &#10007; ERROR
        </span>
      </div>

      <div class="flex items-center gap-2 flex-shrink-0">
        <button
          v-if="scan.status === 'done' || scan.status === 'error'"
          @click.stop="$emit('rerun')"
          class="text-xs px-2 py-1 transition-colors duration-150"
          :style="`color: ${accentColor}; opacity: 0.5; border: 1px solid rgba(${accentRgb}, 0.3); border-radius: 2px;`"
          title="Re-run this scan"
        >
          &#8635;
        </button>
        <svg
          class="w-4 h-4 flex-shrink-0 transition-transform duration-300"
          :class="open ? 'rotate-180' : ''"
          :style="{ color: accentColor, opacity: 0.7 }"
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </button>

    <Transition name="slide">
      <div v-if="open" class="px-5 pb-5">
        <div class="h-px mb-4" :style="{ background: `rgba(${accentRgb}, 0.7)` }"></div>

        <div v-if="scan.status === 'scanning'" class="flex items-center gap-3 py-4">
          <div class="flex gap-1">
            <span v-for="n in 3" :key="n"
              class="w-1.5 h-4 rounded-sm"
              :style="{ background: accentColor, opacity: 0.8, animation: `bounce 1s ease-in-out ${(n-1)*0.15}s infinite` }"
            ></span>
          </div>
          <span class="text-sm" :style="{ color: accentColor }">Running scan&#8230;</span>
        </div>

        <div v-else-if="scan.status === 'error'" class="flex items-start gap-2 py-3">
          <span class="text-red-400 text-lg leading-none">&#9888;</span>
          <div>
            <p class="text-red-400 text-sm font-bold mb-1">SCAN FAILED</p>
            <p class="text-red-500/70 text-xs">{{ scan.error }}</p>
          </div>
        </div>

        <div v-else-if="scan.status === 'done' && scan.data">
          <slot name="results" :data="scan.data" />
        </div>

        <div v-else class="py-3 text-xs" style="color: rgba(0,255,65,0.3)">
          No data available.
        </div>
      </div>
    </Transition>

    <div class="h-px w-full" :style="{ background: `linear-gradient(90deg, transparent, rgba(${accentRgb}, 0.3), transparent)` }"></div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  config: { type: Object, required: true },
  scan:   { type: Object, required: true },
})

defineEmits(['rerun'])

const open = ref(true)

const COLOR_MAP = {
  blue:   { hex: '#00bfff', rgb: '0,191,255' },
  yellow: { hex: '#ffd700', rgb: '255,215,0' },
  red:    { hex: '#ff003c', rgb: '255,0,60' },
  purple: { hex: '#bf00ff', rgb: '191,0,255' },
  green:  { hex: '#00ff41', rgb: '0,255,65' },
  cyan:   { hex: '#00ffff', rgb: '0,255,255' },
}

const colorEntry = computed(() => COLOR_MAP[props.config.color] || COLOR_MAP.green)
const accentColor = computed(() => colorEntry.value.hex)
const accentRgb   = computed(() => colorEntry.value.rgb)

const cardStyle = computed(() => ({
  borderColor: `rgba(${accentRgb.value}, 0.7)`,
  borderWidth: '1px',
  borderStyle: 'solid',
}))
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
}
.slide-enter-to,
.slide-leave-from {
  opacity: 1;
  max-height: 1000px;
}

@keyframes bounce {
  0%, 100% { transform: scaleY(0.4); }
  50%       { transform: scaleY(1); }
}
</style>
