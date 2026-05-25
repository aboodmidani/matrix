<template>
  <div class="relative inline-flex">
    <button
      @click="toggle"
      class="flex items-center gap-1.5 px-3 py-1.5 text-xs transition-all duration-200"
      :style="{
        color: 'rgba(0,255,65,0.5)',
        border: '1px solid rgba(0,255,65,0.2)',
        borderRadius: '2px',
      }"
      :title="'Share ' + label"
      :aria-label="'Share ' + label"
      @mouseenter="open = true"
      @mouseleave="open = false"
    >
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/>
      </svg>
      <span class="hidden sm:inline">Share</span>
    </button>
    <div
      v-if="open"
      class="absolute top-full left-0 mt-1 z-30 flex gap-1 p-1.5"
      :style="{
        background: 'rgba(0,12,3,0.95)',
        border: '1px solid rgba(0,255,65,0.3)',
        borderRadius: '2px',
      }"
    >
      <button @click="share('twitter')" class="px-2 py-1 text-xs transition-colors hover:brightness-125" style="color: rgba(0,255,65,0.6);" :title="'Share on X'">
        X
      </button>
      <button @click="share('linkedin')" class="px-2 py-1 text-xs transition-colors hover:brightness-125" style="color: rgba(0,255,65,0.6);" :title="'Share on LinkedIn'">
        in
      </button>
      <button @click="share('email')" class="px-2 py-1 text-xs transition-colors hover:brightness-125" style="color: rgba(0,255,65,0.6);" :title="'Share via Email'">
        @
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  url: { type: String, default: '' },
  title: { type: String, default: 'Security scan results' },
  label: { type: String, default: 'results' },
})

const open = ref(false)

function toggle() { open.value = !open.value }

function share(platform) {
  open.value = false
  const shareUrl = props.url || window.location.href
  const text = encodeURIComponent(props.title)
  const link = encodeURIComponent(shareUrl)
  let href = ''
  if (platform === 'twitter') {
    href = `https://twitter.com/intent/tweet?text=${text}&url=${link}`
  } else if (platform === 'linkedin') {
    href = `https://linkedin.com/sharing/share-offsite/?url=${link}`
  } else if (platform === 'email') {
    href = `mailto:?subject=${text}&body=${link}`
  }
  if (href) window.open(href, '_blank', 'noopener,noreferrer,width=600,height=400')
}
</script>
