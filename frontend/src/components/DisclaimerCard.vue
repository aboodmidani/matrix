<template>
  <div ref="overlayRef" class="fixed inset-0 z-40 flex items-center justify-center px-4">
    <!-- Backdrop -->
    <div
      ref="backdropRef"
      class="absolute inset-0"
      style="background: rgba(0,0,0,0.85); backdrop-filter: blur(2px); transition: opacity 0.6s ease;"
    ></div>

    <!-- Card -->
    <div
      ref="cardRef"
      class="relative z-10 matrix-card bracket-corners w-full max-w-lg p-8 text-center"
      :style="cardHidden ? 'visibility: hidden;' : ''"
    >
      <!-- Scanline sweep on card -->
      <div class="absolute inset-0 pointer-events-none overflow-hidden" style="border-radius: inherit;">
        <div class="scanline-sweep"></div>
      </div>

      <div class="mb-4 relative">
        <span class="text-xs tracking-[0.4em] uppercase" style="color: rgba(255,215,0,0.5);">⚠ WARNING ⚠</span>
        <h2 class="text-xl font-black mt-2 mb-1" style="font-family: 'Orbitron', monospace; color: #ffd700; letter-spacing: 0.1em;">
          LEGAL DISCLAIMER
        </h2>
        <div class="h-px my-3" style="background: linear-gradient(90deg, transparent, rgba(255,215,0,0.4), transparent);"></div>
      </div>

      <p class="text-sm leading-relaxed mb-6" style="color: rgba(0,255,65,0.7); line-height: 1.8;">
        This tool is intended for <span style="color: #00ff41; font-weight: bold;">educational purposes</span> and
        <span style="color: #00ff41; font-weight: bold;">authorized security testing only</span>.<br><br>
        Only scan systems you own or have explicit written permission to test.
        Unauthorized scanning may be illegal.
      </p>

      <button
        @click="onAccept"
        :disabled="animating"
        class="btn-matrix px-8 py-3 font-bold tracking-[0.25em] text-sm uppercase"
        style="
          background: rgba(0,255,65,0.08);
          border: 1px solid rgba(0,255,65,0.5);
          color: #00ff41;
          font-family: 'Orbitron', monospace;
          border-radius: 2px;
          min-width: 220px;
        "
      >
        [ ACCEPT &amp; CONTINUE ]
      </button>
    </div>

    <!-- Full-screen canvas for the matrix dissolution -->
    <canvas ref="canvasRef" class="fixed inset-0 z-50 pointer-events-none"></canvas>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['accepted'])

const overlayRef  = ref(null)
const backdropRef = ref(null)
const cardRef     = ref(null)
const canvasRef   = ref(null)
const cardHidden  = ref(false)
const animating   = ref(false)

// Matrix characters
const CHARS = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEF<>{}[]|/\\!@#$%^&*'

function onAccept() {
  if (animating.value) return
  animating.value = true

  const card    = cardRef.value
  const canvas  = canvasRef.value
  const overlay = overlayRef.value
  const backdrop = backdropRef.value
  if (!card || !canvas || !overlay) { emit('accepted'); return }

  const rect = card.getBoundingClientRect()

  canvas.width  = window.innerWidth
  canvas.height = window.innerHeight
  const ctx = canvas.getContext('2d')

  // ── Phase 1: Glitch flash (0–300ms) ──────────────────────────────────────
  // Draw the card area with a bright green flash + horizontal glitch lines
  let glitchStart = null
  const GLITCH_DURATION = 300

  function glitchPhase(ts) {
    if (!glitchStart) glitchStart = ts
    const t = (ts - glitchStart) / GLITCH_DURATION

    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Flicker the card area green
    const flashAlpha = Math.sin(t * Math.PI * 8) * 0.5 * (1 - t) + 0.1
    ctx.fillStyle = `rgba(0,255,65,${Math.max(0, flashAlpha)})`
    ctx.fillRect(rect.left - 2, rect.top - 2, rect.width + 4, rect.height + 4)

    // Horizontal glitch slices
    const numSlices = Math.floor(4 + Math.random() * 6)
    for (let i = 0; i < numSlices; i++) {
      const sliceY     = rect.top + Math.random() * rect.height
      const sliceH     = 1 + Math.random() * 4
      const sliceShift = (Math.random() - 0.5) * 20
      const sliceAlpha = 0.3 + Math.random() * 0.5
      ctx.fillStyle = `rgba(0,255,65,${sliceAlpha})`
      ctx.fillRect(rect.left + sliceShift, sliceY, rect.width, sliceH)
    }

    // Random bright scan lines across full width
    if (Math.random() > 0.6) {
      const scanY = rect.top + Math.random() * rect.height
      ctx.fillStyle = 'rgba(0,255,200,0.15)'
      ctx.fillRect(0, scanY, canvas.width, 1)
    }

    if (t < 1) {
      requestAnimationFrame(glitchPhase)
    } else {
      // Hide card, start matrix rain phase
      cardHidden.value = true
      requestAnimationFrame(() => requestAnimationFrame(startRainPhase))
    }
  }

  requestAnimationFrame(glitchPhase)

  // ── Phase 2: Matrix rain dissolution ─────────────────────────────────────
  function startRainPhase() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    const FONT_SIZE = 13
    const cols = Math.ceil(rect.width / FONT_SIZE)

    // Each column: starts at top of card, falls down
    const columns = Array.from({ length: cols }, (_, i) => ({
      x:       rect.left + i * FONT_SIZE,
      y:       rect.top,
      speed:   0.4 + Math.random() * 1.2,
      length:  Math.floor(rect.height / FONT_SIZE) + Math.floor(Math.random() * 8),
      chars:   Array.from({ length: 30 }, () => CHARS[Math.floor(Math.random() * CHARS.length)]),
      head:    0,
      delay:   Math.random() * 0.3,
      elapsed: 0,
      done:    false,
    }))

    const RAIN_DURATION = 1.8  // seconds total
    let lastTime = null

    // Fade backdrop while rain falls
    if (backdrop) {
      backdrop.style.transition = 'opacity 1.2s ease'
      backdrop.style.opacity = '0'
    }

    function rainPhase(ts) {
      if (!lastTime) lastTime = ts
      const dt = Math.min((ts - lastTime) / 1000, 0.05)
      lastTime = ts

      // Dim previous frame (trail effect)
      ctx.fillStyle = 'rgba(0,0,0,0.18)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      ctx.font = `${FONT_SIZE}px "Share Tech Mono", monospace`

      let anyActive = false

      for (const col of columns) {
        col.elapsed += dt
        if (col.elapsed < col.delay) { anyActive = true; continue }

        const progress = (col.elapsed - col.delay) / RAIN_DURATION
        if (progress >= 1) { col.done = true; continue }

        anyActive = true
        col.head += col.speed

        // Randomize chars occasionally
        if (Math.random() > 0.85) {
          col.chars[Math.floor(Math.random() * col.chars.length)] =
            CHARS[Math.floor(Math.random() * CHARS.length)]
        }

        // Draw the column of characters
        const trailLen = Math.min(col.length, Math.floor(col.head))
        for (let j = 0; j < trailLen; j++) {
          const charY = rect.top + (col.head - j) * FONT_SIZE
          if (charY < rect.top - FONT_SIZE || charY > canvas.height + FONT_SIZE) continue

          const charIdx = j % col.chars.length
          const char    = col.chars[charIdx]

          // Head char: bright white-green
          if (j === 0) {
            ctx.fillStyle = `rgba(200,255,220,${1 - progress * 0.5})`
          } else if (j < 3) {
            ctx.fillStyle = `rgba(0,255,65,${(1 - j / trailLen) * (1 - progress * 0.7)})`
          } else {
            const fade = (1 - j / trailLen) * (1 - progress)
            ctx.fillStyle = `rgba(0,${Math.floor(150 + Math.random() * 80)},40,${fade})`
          }

          ctx.fillText(char, col.x, charY)
        }
      }

      if (anyActive) {
        requestAnimationFrame(rainPhase)
      } else {
        // Final fade out
        let fadeStart = null
        function fadeOut(ts) {
          if (!fadeStart) fadeStart = ts
          const t = (ts - fadeStart) / 400
          ctx.fillStyle = `rgba(0,0,0,${Math.min(t * 0.3, 0.3)})`
          ctx.fillRect(0, 0, canvas.width, canvas.height)
          if (t < 1) {
            requestAnimationFrame(fadeOut)
          } else {
            ctx.clearRect(0, 0, canvas.width, canvas.height)
            emit('accepted')
          }
        }
        requestAnimationFrame(fadeOut)
      }
    }

    requestAnimationFrame(rainPhase)
  }
}
</script>

<style scoped>
/* Scanline sweep animation on the card */
.scanline-sweep {
  position: absolute;
  top: -100%;
  left: 0;
  right: 0;
  height: 40%;
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(0, 255, 65, 0.04) 40%,
    rgba(0, 255, 65, 0.08) 50%,
    rgba(0, 255, 65, 0.04) 60%,
    transparent 100%
  );
  animation: sweep 4s linear infinite;
  pointer-events: none;
}

@keyframes sweep {
  0%   { top: -40%; }
  100% { top: 100%; }
}

/* Card entrance */
.matrix-card {
  animation: cardIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes cardIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.97);
    filter: brightness(2);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: brightness(1);
  }
}
</style>
