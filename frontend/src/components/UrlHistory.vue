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
        :ref="el => { if (el) itemRefs[i] = el }"
        @click="$emit('select', item)"
        class="flex items-center gap-2 px-3 py-2 text-xs cursor-pointer transition-colors duration-100"
        :style="{
          color: i === 0 ? '#00ff41' : 'rgba(0,255,65,0.6)',
          borderBottom: i < history.length - 1 ? '1px solid rgba(0,255,65,0.06)' : 'none',
          animation: revealed[i] ? `holoItemIn 0.4s cubic-bezier(0.16,1,0.3,1) ${i * 0.05}s forwards` : 'none',
          opacity: revealed[i] ? 1 : 0,
          transform: revealed[i] ? 'translateY(0)' : 'translateY(-8px)',
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
import { ref, onMounted, nextTick } from 'vue'

const props = defineProps({
  history: { type: Array, default: () => [] },
})
defineEmits(['select', 'remove'])

const itemRefs = ref({})
const revealed = ref([])

onMounted(async () => {
  await nextTick()
  revealed.value = props.history.map(() => true)
})
</script>

<style scoped>
@keyframes holoItemIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
    filter: brightness(1.5);
  }
  to {
    opacity: 1;
    transform: translateY(0);
    filter: brightness(1);
  }
}
</style>
