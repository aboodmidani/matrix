<template>
  <div class="min-h-screen bg-black text-green-400 font-mono overflow-hidden relative">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
