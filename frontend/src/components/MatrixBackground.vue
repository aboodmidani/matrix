<template>
  <canvas ref="canvasRef" class="fixed inset-0 z-0 pointer-events-none" :style="parallaxStyle"></canvas>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useMouse, useScroll } from '@vueuse/core'

const canvasRef = ref(null)
let animationId = null
let resizeHandler = null

const { x: mouseX, y: mouseY } = useMouse()
const { y: scrollY } = useScroll()

const isMobile = window.innerWidth < 768
const DROPS_PER_COL = 3
const LAYERS = [
  { speed: 0.25, opacity: 0.3, fontSize: 9, chars: '0123456789ABCDEF<>[]{}' },
  { speed: 0.5, opacity: 0.6, fontSize: 13, chars: 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEF<>{}[]|/\\' },
  { speed: 0.8, opacity: 0.4, fontSize: 18, chars: '01アイウエオ' },
]

let ctx = null
let widths = []
let allDrops = []

function resize() {
  if (!canvasRef.value) return
  canvasRef.value.width = window.innerWidth
  canvasRef.value.height = window.innerHeight
  ctx = canvasRef.value.getContext('2d')
  widths = LAYERS.map(l => Math.floor(canvasRef.value.width / (l.fontSize * 0.6)))
  allDrops = widths.map((cols, li) =>
    Array.from({ length: cols * DROPS_PER_COL }, () => ({
      col: Math.floor(Math.random() * cols),
      y: Math.random() * -canvasRef.value.height * (1 + Math.random()),
      speed: LAYERS[li].speed * (0.6 + Math.random() * 0.8),
      charIdx: Math.floor(Math.random() * LAYERS[li].chars.length),
    }))
  )
}

onMounted(() => {
  resize()
  resizeHandler = resize
  window.addEventListener('resize', resizeHandler)

  function draw() {
    if (!ctx || !canvasRef.value) { animationId = requestAnimationFrame(draw); return }
    ctx.fillStyle = 'rgba(0, 0, 0, 0.035)'
    ctx.fillRect(0, 0, canvasRef.value.width, canvasRef.value.height)

    for (let li = 0; li < LAYERS.length; li++) {
      const layer = LAYERS[li]
      const drops = allDrops[li]
      const cols = widths[li]

      ctx.font = `${layer.fontSize}px "Share Tech Mono", monospace`
      ctx.globalAlpha = layer.opacity

      for (const drop of drops) {
        const char = layer.chars[drop.charIdx]
        const x = drop.col * layer.fontSize * 0.6
        const y = drop.y * layer.fontSize

        if (Math.random() > 0.97) {
          drop.charIdx = Math.floor(Math.random() * layer.chars.length)
        }

        if (li === 0 || li === LAYERS.length - 1) {
          ctx.fillStyle = '#00ff41'
        } else {
          const r = Math.random()
          ctx.fillStyle = r > 0.95 ? '#ccffdd' : r > 0.7 ? '#00ff41' : '#00b32c'
        }

        ctx.fillText(char, x, y)

        if (y > canvasRef.value.height + 20 && Math.random() > 0.98) {
          drop.y = -10
          drop.col = Math.floor(Math.random() * cols)
        }
        drop.y += drop.speed
      }
      ctx.globalAlpha = 1
    }

    animationId = requestAnimationFrame(draw)
  }

  draw()
})

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
})

const parallaxStyle = computed(() => {
  if (isMobile) return {}
  const mx = (mouseX.value / window.innerWidth - 0.5) * 2
  const my = (mouseY.value / window.innerHeight - 0.5) * 2
  const sy = scrollY.value * 0.08
  return {
    transform: `translate3d(${mx * 8}px, ${my * 8 + sy}px, 0)`,
    transition: 'transform 0.15s ease-out',
  }
})
</script>

<style scoped>
canvas {
  opacity: 0.18;
}
@media (max-width: 640px) {
  canvas { opacity: 0.08; }
}
</style>
