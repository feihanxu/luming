<template>
  <div class="person-card fade-in" @click="$emit('click')">
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

const avatarColors = [
  'linear-gradient(135deg, #7C9A92 0%, #9DB5AD 100%)',
  'linear-gradient(135deg, #A390C4 0%, #C4B5D9 100%)',
  'linear-gradient(135deg, #7BA3C9 0%, #9DBED9 100%)',
  'linear-gradient(135deg, #D4A574 0%, #E5C4A4 100%)',
  'linear-gradient(135deg, #C9707D 0%, #D999A3 100%)'
]

const avatarStyle = computed(() => {
  if (props.person.avatar) {
    return { backgroundImage: `url(${props.person.avatar})`, backgroundSize: 'cover' }
  }
  const colorIndex = props.person.name.charCodeAt(0) % avatarColors.length
  return { background: avatarColors[colorIndex] }
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
  background: var(--card);
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 0 16px 12px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.person-card:active {
  transform: scale(0.98);
  box-shadow: var(--shadow-md);
}

.person-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  color: white;
  flex-shrink: 0;
}

.person-info {
  flex: 1;
  min-width: 0;
}

.person-name {
  font-size: 17px;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.person-meta {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.person-badge {
  font-size: 13px;
  color: var(--text-tertiary);
  flex-shrink: 0;
  padding: 4px 10px;
  background: var(--bg-secondary);
  border-radius: 20px;
}

.person-badge.warning {
  color: var(--orange);
  background: rgba(212, 165, 116, 0.15);
}
</style>
