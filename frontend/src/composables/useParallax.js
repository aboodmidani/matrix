import { useMouse, useScroll } from '@vueuse/core'
import { computed } from 'vue'

export function useParallax({ mouseSensitivity = 0.025, scrollFactor = 0.12 } = {}) {
  const { x: mouseX, y: mouseY } = useMouse()
  const { y: scrollY } = useScroll()

  const isMobile = window.innerWidth < 768

  const transform = computed(() => {
    if (isMobile) return ''
    const mx = (mouseX.value / window.innerWidth - 0.5) * 2
    const my = (mouseY.value / window.innerHeight - 0.5) * 2
    const sy = scrollY.value * scrollFactor
    return `translate3d(${mx * mouseSensitivity * 100}px, ${my * mouseSensitivity * 100 + sy}px, 0)`
  })

  const depthTransforms = computed(() => {
    if (isMobile) return { far: '', mid: '', near: '' }
    const mx = (mouseX.value / window.innerWidth - 0.5) * 2
    const my = (mouseY.value / window.innerHeight - 0.5) * 2
    return {
      far: `translate3d(${mx * 4}px, ${my * 4 + scrollY.value * 0.06}px, 0)`,
      mid: `translate3d(${mx * 12}px, ${my * 12 + scrollY.value * 0.12}px, 0)`,
      near: `translate3d(${mx * 24}px, ${my * 24 + scrollY.value * 0.2}px, 0)`,
    }
  })

  return { parallaxTransform: transform, depthTransforms }
}
