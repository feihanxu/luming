<template>
  <div class="record-card" @click="$emit('click')">
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
  background: var(--bg);
  margin-bottom: 1px;
  padding: 14px 16px;
  cursor: pointer;
  transition: background 0.1s ease;
}

.record-card:active {
  background: var(--bg-secondary);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 6px;
}

.record-person-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.record-person {
  font-size: 17px;
  font-weight: 500;
}

.record-company {
  font-size: 13px;
  color: var(--text-secondary);
}

.record-time {
  font-size: 15px;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.record-summary {
  font-size: 15px;
  color: var(--text-secondary);
  margin-bottom: 10px;
}

.record-structured {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.struct-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.struct-label {
  font-size: 13px;
  color: var(--text-tertiary);
  min-width: 48px;
}

.struct-value {
  font-size: 15px;
  color: var(--text);
}

.struct-value.todo {
  color: var(--accent);
}
</style>
