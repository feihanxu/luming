<template>
  <div class="app">
    <div class="phone-frame">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
      
      <BottomNav />
    </div>
  </div>
</template>

<script setup>
import BottomNav from './components/BottomNav.vue'
</script>
