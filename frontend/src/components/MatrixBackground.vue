<template>
  <canvas ref="canvas" class="fixed inset-0 z-0"></canvas>
</template>

<script>
import { onMounted, onUnmounted, ref } from 'vue'

export default {
  name: 'MatrixBackground',
  setup() {
    const canvas = ref(null)
    let animationId = null

    onMounted(() => {
      initMatrixRain()
    })

    onUnmounted(() => {
      if (animationId) {
        cancelAnimationFrame(animationId)
      }
    })

    function initMatrixRain() {
      const ctx = canvas.value.getContext('2d')
      
      // Set canvas size
      const resizeCanvas = () => {
        canvas.value.width = window.innerWidth
        canvas.value.height = window.innerHeight
      }
      resizeCanvas()
      window.addEventListener('resize', resizeCanvas)

      // Matrix characters
      const matrix = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()_+-=[]{}|;:,.<>?'
      const chars = matrix.split('')
      const fontSize = 14
      const columns = Math.floor(canvas.value.width / fontSize)
      const drops = Array(columns).fill(1)

      // Animation loop
      const draw = () => {
        // Semi-transparent black background for trail effect
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)'
        ctx.fillRect(0, 0, canvas.value.width, canvas.value.height)

        // Green text
        ctx.fillStyle = '#00ff41'
        ctx.font = `${fontSize}px monospace`

        // Draw characters
        for (let i = 0; i < drops.length; i++) {
          const char = chars[Math.floor(Math.random() * chars.length)]
          const x = i * fontSize
          const y = drops[i] * fontSize

          ctx.fillText(char, x, y)

          // Reset drop to top randomly
          if (y > canvas.value.height && Math.random() > 0.975) {
            drops[i] = 0
          }
          drops[i]++
        }

        animationId = requestAnimationFrame(draw)
      }

      draw()
    }

    return {
      canvas
    }
  }
}
</script>

<style scoped>
canvas {
  opacity: 0.15;
  pointer-events: none;
}
</style>
