<template>
  <div class="person-card" @click="$emit('click')">
    <div class="person-avatar" :style="avatarStyle">
      {{ person.name.charAt(0) }}
    </div>
    <div class="person-info">
      <div class="person-name">{{ person.name }}</div>
      <div class="person-meta">{{ person.title }} · {{ person.company }}</div>
    </div>
    <div class="person-badge" :class="{ warning: isStale }">
      {{ lastContactText }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  person: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

const avatarStyle = computed(() => {
  if (props.person.avatar) {
    return { backgroundImage: `url(${props.person.avatar})`, backgroundSize: 'cover' }
  }
  return {}
})

const lastContactText = computed(() => {
  const last = new Date(props.person.lastContact)
  const now = new Date()
  const diffDays = Math.floor((now - last) / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return '今天'
  if (diffDays === 1) return '昨天'
  if (diffDays < 7) return `${diffDays}天前`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前`
  return `${Math.floor(diffDays / 30)}个月前`
})

const isStale = computed(() => {
  const last = new Date(props.person.lastContact)
  const thirtyDaysAgo = new Date()
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)
  return last < thirtyDaysAgo
})
</script>

<style scoped>
.person-card {
  background: var(--bg);
  padding: 14px 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 1px;
  cursor: pointer;
  transition: background 0.1s ease;
}

.person-card:active {
  background: var(--bg-secondary);
}

.person-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #E0E0E0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 500;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.person-info {
  flex: 1;
  min-width: 0;
}

.person-name {
  font-size: 17px;
  font-weight: 500;
}

.person-meta {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.person-badge {
  font-size: 14px;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.person-badge.warning {
  color: var(--orange);
}
</style>
