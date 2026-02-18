<template>
  <!-- Fixed full-screen overlay — always centered -->
  <div ref="overlayRef" class="fixed inset-0 z-40 flex items-center justify-center px-4">
    <!-- Backdrop -->
    <div class="absolute inset-0" style="background: rgba(0,0,0,0.85); backdrop-filter: blur(2px);"></div>

    <!-- Card — hidden once animation starts -->
    <div
      ref="cardRef"
      class="relative z-10 matrix-card bracket-corners w-full max-w-lg p-8 text-center scanline fade-in-up"
      :style="cardHidden ? 'visibility: hidden;' : ''"
    >
      <div class="mb-4">
        <span class="text-xs tracking-[0.3em] uppercase" style="color: rgba(255,215,0,0.5);">⚠ WARNING ⚠</span>
        <h2 class="text-xl font-bold mt-2 mb-1" style="font-family: 'Orbitron', monospace; color: #ffd700;">
          LEGAL DISCLAIMER
        </h2>
        <div class="h-px my-3" style="background: linear-gradient(90deg, transparent, rgba(255,215,0,0.3), transparent);"></div>
      </div>

      <p class="text-sm leading-relaxed mb-6" style="color: rgba(0,255,65,0.7);">
        This tool is intended for <span style="color: #00ff41;">educational purposes</span> and
        <span style="color: #00ff41;">authorized security testing only</span>.<br><br>
        Only scan systems you own or have explicit written permission to test.
        Unauthorized scanning may be illegal.
      </p>

      <button
        @click="startDisintegration"
        :disabled="animating"
        class="btn-matrix px-8 py-3 font-bold tracking-widest text-sm uppercase"
        style="
          background: rgba(0,255,65,0.1);
          border: 1px solid rgba(0,255,65,0.5);
          color: #00ff41;
          font-family: 'Orbitron', monospace;
        "
      >
        [ ACCEPT &amp; CONTINUE ]
      </button>
    </div>

    <!-- Canvas sits above the card, z-50 -->
    <canvas
      ref="canvasRef"
      class="fixed inset-0 z-50 pointer-events-none"
    ></canvas>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['accepted'])

const overlayRef = ref(null)
const cardRef    = ref(null)
const canvasRef  = ref(null)
const animating  = ref(false)
const cardHidden = ref(false)

function startDisintegration() {
  if (animating.value) return
  animating.value = true

  const card    = cardRef.value
  const canvas  = canvasRef.value
  const overlay = overlayRef.value
  if (!card || !canvas || !overlay) { emit('accepted'); return }

  const rect = card.getBoundingClientRect()

  // Full-screen canvas
  canvas.width  = window.innerWidth
  canvas.height = window.innerHeight
  const ctx = canvas.getContext('2d')

  // Build a dense grid of particles covering the card area
  // Use colors sampled from the card's visual design
  const PIXEL = 5
  const cols  = Math.ceil(rect.width  / PIXEL)
  const rows  = Math.ceil(rect.height / PIXEL)
  const particles = []

  // Color palette matching the card's actual appearance
  const greenPalette  = ['#00ff41','#00e639','#00cc33','#00b32c','#009926','#007a1f','rgba(0,255,65,0.9)','rgba(0,255,65,0.6)']
  const goldPalette   = ['#ffd700','#ffcc00','rgba(255,215,0,0.8)','rgba(255,215,0,0.5)']
  const cyanPalette   = ['#00ffcc','#00bfff','rgba(0,191,255,0.7)']
  const darkPalette   = ['rgba(0,10,2,0.95)','rgba(0,20,5,0.9)','rgba(0,30,8,0.85)']

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x = rect.left + c * PIXEL
      const y = rect.top  + r * PIXEL
      const rowFrac = r / rows
      const colFrac = c / cols

      // Determine color zone based on position in card
      let palette
      if (rowFrac < 0.08) {
        // Top area — gold (warning text)
        palette = Math.random() > 0.4 ? goldPalette : darkPalette
      } else if (rowFrac < 0.22) {
        // Title area — gold + green mix
        palette = Math.random() > 0.5 ? goldPalette : greenPalette
      } else if (rowFrac > 0.85) {
        // Button area — bright green
        palette = Math.random() > 0.3 ? greenPalette : cyanPalette
      } else if (colFrac < 0.05 || colFrac > 0.95 || rowFrac < 0.02 || rowFrac > 0.98) {
        // Border edges — bright green
        palette = greenPalette
      } else {
        // Body — mostly dark with green/cyan accents
        const rnd = Math.random()
        if (rnd > 0.85)      palette = greenPalette
        else if (rnd > 0.75) palette = cyanPalette
        else                 palette = darkPalette
      }

      const color = palette[Math.floor(Math.random() * palette.length)]

      // Explosion direction — radiate outward from card center
      const cx = rect.left + rect.width  / 2
      const cy = rect.top  + rect.height / 2
      const dx = x - cx
      const dy = y - cy
      const dist = Math.sqrt(dx * dx + dy * dy) || 1
      const baseAngle = Math.atan2(dy, dx)
      const spread = (Math.random() - 0.5) * 1.2  // ±0.6 rad spread
      const angle  = baseAngle + spread
      const speed  = 1.5 + Math.random() * 8 + (dist / Math.max(rect.width, rect.height)) * 4

      particles.push({
        x, y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 1,
        size: PIXEL * (0.5 + Math.random()),
        color,
        alpha: 1,
        rotation: Math.random() * Math.PI * 2,
        spin: (Math.random() - 0.5) * 0.4,
        delay: (dist / Math.max(rect.width, rect.height)) * 0.2 + Math.random() * 0.15,
        elapsed: 0,
      })
    }
  }

  // Hide the card on the very next frame (after canvas is ready)
  requestAnimationFrame(() => {
    cardHidden.value = true
  })

  const DURATION = 1.5
  let lastTime = null
  let started = false

  function animate(ts) {
    if (!lastTime) lastTime = ts
    const dt = Math.min((ts - lastTime) / 1000, 0.05)
    lastTime = ts

    // Wait one extra frame before starting so cardHidden takes effect
    if (!started) {
      started = true
      requestAnimationFrame(animate)
      return
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height)

    let allDone = true

    for (const p of particles) {
      p.elapsed += dt
      if (p.elapsed < p.delay) { allDone = false; continue }

      const t = (p.elapsed - p.delay) / DURATION
      if (t >= 1) continue

      allDone = false

      p.x  += p.vx
      p.y  += p.vy
      p.vy += 0.1
      p.vx *= 0.99
      p.rotation += p.spin
      p.alpha = Math.max(0, 1 - t * t)

      ctx.save()
      ctx.globalAlpha = p.alpha
      ctx.translate(p.x + p.size / 2, p.y + p.size / 2)
      ctx.rotate(p.rotation)
      ctx.fillStyle = p.color
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size)
      ctx.restore()
    }

    if (allDone) {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      emit('accepted')
    } else {
      requestAnimationFrame(animate)
    }
  }

  requestAnimationFrame(animate)
}
</script>
