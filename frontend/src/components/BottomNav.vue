<template>
  <nav class="bottom-nav">
    <router-link 
      v-for="item in navItems" 
      :key="item.path"
      :to="item.path"
      class="nav-item"
      :class="{ active: isActive(item.path) }"
    >
      <span class="nav-icon">{{ item.icon }}</span>
      <span class="nav-label">{{ item.label }}</span>
    </router-link>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { path: '/timeline', icon: '○', label: '时间轴' },
  { path: '/people', icon: '◇', label: '人脉' },
  { path: '/chat', icon: '☆', label: '呦呦' },
  { path: '/profile', icon: '○', label: '我的' }
]

const isActive = (path) => {
  return route.path === path
}
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 430px;
  background: var(--bg);
  border-top: 0.5px solid var(--separator);
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
  padding-bottom: calc(8px + env(safe-area-inset-bottom));
  z-index: 1000;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4px 16px;
  text-decoration: none;
  color: var(--text-secondary);
  transition: color 0.1s ease;
}

.nav-item.active {
  color: var(--accent);
}

.nav-icon {
  font-size: 24px;
  font-weight: 400;
  margin-bottom: 2px;
}

.nav-label {
  font-size: 10px;
}
</style>
