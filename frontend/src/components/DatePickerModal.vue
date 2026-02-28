<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-sheet">
      <div class="modal-header">
        <span class="modal-title">选择日期</span>
        <button class="modal-close" @click="$emit('close')">取消</button>
      </div>
      <div class="modal-body">
        <div class="date-picker-row">
          <div class="date-picker-col">
            <div class="date-picker-label">年</div>
            <select v-model="selectedYear" class="date-picker-select">
              <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
            </select>
          </div>
          <div class="date-picker-col">
            <div class="date-picker-label">月</div>
            <select v-model="selectedMonth" class="date-picker-select">
              <option v-for="month in 12" :key="month" :value="month">{{ month }}月</option>
            </select>
          </div>
          <div class="date-picker-col">
            <div class="date-picker-label">日</div>
            <select v-model="selectedDay" class="date-picker-select">
              <option v-for="day in daysInMonth" :key="day" :value="day">{{ day }}</option>
            </select>
          </div>
        </div>
        <div class="date-picker-actions">
          <button class="date-picker-btn cancel" @click="$emit('close')">取消</button>
          <button class="date-picker-btn confirm" @click="confirm">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['close', 'select'])

const now = new Date()
const selectedYear = ref(now.getFullYear())
const selectedMonth = ref(now.getMonth() + 1)
const selectedDay = ref(now.getDate())

const years = computed(() => {
  const currentYear = now.getFullYear()
  return Array.from({ length: 5 }, (_, i) => currentYear - i)
})

const daysInMonth = computed(() => {
  const days = new Date(selectedYear.value, selectedMonth.value, 0).getDate()
  return days
})

function confirm() {
  const date = new Date(selectedYear.value, selectedMonth.value - 1, selectedDay.value)
  emit('select', { 
    start: date.toISOString().split('T')[0],
    end: date.toISOString().split('T')[0]
  })
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 2000;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.modal-sheet {
  width: 100%;
  max-width: 430px;
  background: var(--bg);
  border-radius: 12px 12px 0 0;
  animation: slideUp 0.25s ease;
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 0.5px solid var(--separator);
}

.modal-title {
  font-size: 17px;
  font-weight: 600;
}

.modal-close {
  font-size: 17px;
  color: var(--accent);
  background: none;
  border: none;
  cursor: pointer;
}

.modal-body {
  padding: 16px;
}

.date-picker-row {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.date-picker-col {
  flex: 1;
}

.date-picker-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.date-picker-select {
  width: 100%;
  padding: 12px;
  background: var(--bg-secondary);
  border: none;
  border-radius: 8px;
  font-size: 16px;
  color: var(--text);
  cursor: pointer;
}

.date-picker-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.date-picker-btn {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
}

.date-picker-btn.cancel {
  background: var(--bg-secondary);
  color: var(--text);
}

.date-picker-btn.confirm {
  background: var(--accent);
  color: white;
}
</style>
