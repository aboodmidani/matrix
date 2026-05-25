import { ref, onMounted, onUnmounted } from 'vue'

export function useReveal(options = {}) {
  const { threshold = 0.12, delay = 0, once = true } = options
  const elementRef = ref(null)
  const isRevealed = ref(false)
  let observer = null

  onMounted(() => {
    const el = elementRef.value
    if (!el) return
    observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setTimeout(() => { isRevealed.value = true }, delay)
          if (once) observer.unobserve(entry.target)
        } else if (!once) {
          isRevealed.value = false
        }
      },
      { threshold }
    )
    observer.observe(el)
  })

  onUnmounted(() => {
    if (observer) observer.disconnect()
  })

  return { elementRef, isRevealed }
}
