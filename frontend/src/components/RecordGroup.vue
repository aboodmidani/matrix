<template>
  <div v-if="items && items.length" class="mb-3">
    <div class="flex items-center gap-2 mb-2">
      <div class="w-1 h-3" style="background: var(--matrix-green-dim);"></div>
      <p class="text-xs tracking-widest uppercase" style="color: rgba(0,255,65,0.5);">{{ label }}</p>
      <span class="text-xs px-1.5 py-0.5 rounded" style="background: rgba(0,255,65,0.08); color: rgba(0,255,65,0.5); border: 1px solid rgba(0,255,65,0.15);">
        {{ items.length }}
      </span>
    </div>
    <div class="flex flex-wrap gap-1.5">
      <span
        v-for="item in items"
        :key="item"
        class="chip"
        style="color: #00bfff; background: rgba(0,191,255,0.06); border-color: rgba(0,191,255,0.2);"
      >
        {{ item }}
      </span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  items: { type: Array, default: () => [] },
})
</script>
