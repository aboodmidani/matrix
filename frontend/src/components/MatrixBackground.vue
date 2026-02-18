<template>
  <canvas ref="canvas" class="fixed inset-0 z-0 pointer-events-none"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let animationId = null
let resizeHandler = null

onMounted(() => {
  const ctx = canvas.value.getContext('2d')

  // Characters — mix of katakana, latin, digits for authentic look
  const CHARS = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEF<>{}[]|/\\'.split('')
  const FONT_SIZE = 13
  let columns, drops

  function resize() {
    canvas.value.width  = window.innerWidth
    canvas.value.height = window.innerHeight
    columns = Math.floor(canvas.value.width / FONT_SIZE)
    drops   = Array(columns).fill(0).map(() => Math.random() * -50)
  }

  resize()
  resizeHandler = resize
  window.addEventListener('resize', resizeHandler)

  function draw() {
    // Fade trail
    ctx.fillStyle = 'rgba(0, 0, 0, 0.04)'
    ctx.fillRect(0, 0, canvas.value.width, canvas.value.height)

    ctx.font = `${FONT_SIZE}px "Share Tech Mono", monospace`

    for (let i = 0; i < drops.length; i++) {
      const char = CHARS[Math.floor(Math.random() * CHARS.length)]
      const x = i * FONT_SIZE
      const y = drops[i] * FONT_SIZE

      // Leading character is bright white-green
      if (Math.random() > 0.95) {
        ctx.fillStyle = '#ccffdd'
      } else if (Math.random() > 0.7) {
        ctx.fillStyle = '#00ff41'
      } else {
        ctx.fillStyle = '#00b32c'
      }

      ctx.fillText(char, x, y)

      // Reset drop randomly after it passes the bottom
      if (y > canvas.value.height && Math.random() > 0.97) {
        drops[i] = 0
      }
      drops[i] += 0.5
    }

    animationId = requestAnimationFrame(draw)
  }

  draw()
})

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
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
