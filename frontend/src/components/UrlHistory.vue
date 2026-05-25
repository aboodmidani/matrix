<template>
  <div v-if="history.length" class="relative">
    <div
      class="absolute top-full left-0 right-0 z-20 mt-0.5 overflow-hidden"
      :style="{
        background: 'rgba(0,12,3,0.96)',
        border: '1px solid rgba(0,255,65,0.3)',
        borderRadius: '2px',
      }"
    >
      <div
        v-for="(item, i) in history"
        :key="i"
        @click="$emit('select', item)"
        class="flex items-center gap-2 px-3 py-2 text-xs cursor-pointer transition-colors duration-100"
        :style="{
          color: i === 0 ? '#00ff41' : 'rgba(0,255,65,0.6)',
          borderBottom: i < history.length - 1 ? '1px solid rgba(0,255,65,0.06)' : 'none',
        }"
        @mouseenter="$event.target.style.background = 'rgba(0,255,65,0.06)'"
        @mouseleave="$event.target.style.background = 'transparent'"
      >
        <span style="color: rgba(0,255,65,0.3);">&#8635;</span>
        <span class="truncate">{{ item }}</span>
          <button
            @click.stop="$emit('remove', i)"
            class="ml-auto flex-shrink-0 px-1 transition-colors"
            style="color: rgba(255,0,60,0.4);"
            :aria-label="'Remove ' + item"
          >
          &#10005;
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  history: { type: Array, default: () => [] },
})
defineEmits(['select', 'remove'])
</script>
