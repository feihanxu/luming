<template>
  <div class="record-card fade-in" @click="$emit('click')">
    <div class="record-header">
      <div class="record-person-info">
        <span class="record-person">{{ record.personName }}</span>
        <span v-if="record.personTitle || record.personCompany" class="record-company">
          {{ record.personTitle }} · {{ record.personCompany }}
        </span>
      </div>
      <span class="record-time">{{ formatTime(record.timestamp) }}</span>
    </div>
    <div class="record-summary">{{ record.summary }}</div>
    <div class="record-structured">
      <div v-if="record.location" class="struct-row">
        <span class="struct-label">地点</span>
        <span class="struct-value">{{ record.location }}</span>
      </div>
      <div v-if="record.topic" class="struct-row">
        <span class="struct-label">事项</span>
        <span class="struct-value">{{ record.topic }}</span>
      </div>
      <div v-if="record.todo" class="struct-row">
        <span class="struct-label">待办</span>
        <span class="struct-value todo">{{ record.todo }}</span>
      </div>
      <div v-if="record.note" class="struct-row">
        <span class="struct-label">备注</span>
        <span class="struct-value">{{ record.note }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  record: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.record-card {
  background: var(--card);
  margin: 0 16px 12px;
  padding: 18px 20px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.record-card:active {
  transform: scale(0.98);
  box-shadow: var(--shadow-md);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.record-person-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.record-person {
  font-size: 17px;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.record-company {
  font-size: 13px;
  color: var(--text-secondary);
}

.record-time {
  font-size: 14px;
  color: var(--text-tertiary);
  flex-shrink: 0;
  padding: 4px 10px;
  background: var(--bg-secondary);
  border-radius: 20px;
}

.record-summary {
  font-size: 15px;
  color: var(--text-secondary);
  margin-bottom: 14px;
  line-height: 1.5;
}

.record-structured {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.struct-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.struct-label {
  font-size: 13px;
  color: var(--text-tertiary);
  min-width: 48px;
  font-weight: 500;
}

.struct-value {
  font-size: 15px;
  color: var(--text);
  line-height: 1.4;
}

.struct-value.todo {
  color: var(--accent);
  font-weight: 500;
}
</style>
