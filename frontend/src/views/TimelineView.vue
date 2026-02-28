<template>
  <div class="timeline-page">
    <div class="page-header">
      <div class="page-title">时间轴</div>
    </div>

    <div class="search-bar">
      <input type="text" class="search-input" placeholder="搜索记录..." v-model="searchQuery">
    </div>

    <div class="date-filter">
      <button 
        v-for="filter in dateFilters" 
        :key="filter.value"
        class="date-filter-btn"
        :class="{ active: activeFilter === filter.value }"
        @click="setFilter(filter.value)"
      >
        {{ filter.label }}
      </button>
      <div class="date-filter-custom">
        <button class="date-picker-btn" @click="showDatePicker = true">
          {{ formatDateRange.start || '开始日期' }}
        </button>
        <span class="date-sep">→</span>
        <button class="date-picker-btn" @click="showDatePicker = true">
          {{ formatDateRange.end || '结束日期' }}
        </button>
      </div>
    </div>

    <div class="timeline-container">
      <div class="timeline-content">
        <div v-for="(records, date) in groupedRecords" :key="date">
          <div class="date-section">{{ formatDate(date) }}</div>
          <RecordCard 
            v-for="record in records" 
            :key="record.id" 
            :record="record"
            @click="goToPerson(record.personId)"
          />
        </div>
        
        <div v-if="Object.keys(groupedRecords).length === 0" class="empty-state">
          <div class="empty-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M8 15s1.5 2 4 2 4-2 4-2"/>
              <line x1="9" y1="9" x2="9.01" y2="9"/>
              <line x1="15" y1="9" x2="15.01" y2="9"/>
            </svg>
          </div>
          <div class="empty-text">暂无记录</div>
          <div class="empty-hint">在"呦呦"中记录你今天见了谁</div>
        </div>
      </div>

      <div class="timeline-scroller">
        <div 
          v-for="month in months" 
          :key="month"
          class="scroller-item"
          :class="{ active: scrollToMonth === month }"
          @click="scrollTo(month)"
        >
          {{ month }}
        </div>
        <div class="scroller-track"></div>
      </div>
    </div>

    <DatePickerModal 
      v-if="showDatePicker"
      @close="showDatePicker = false"
      @select="setDateRange"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRecordStore } from '../stores/record'
import RecordCard from '../components/RecordCard.vue'
import DatePickerModal from '../components/DatePickerModal.vue'

const router = useRouter()
const recordStore = useRecordStore()

const searchQuery = ref('')
const activeFilter = ref('all')
const showDatePicker = ref(false)
const dateRange = ref({ start: null, end: null })
const scrollToMonth = ref('')

const dateFilters = [
  { label: '全部', value: 'all' },
  { label: '本周', value: 'week' },
  { label: '本月', value: 'month' }
]

const months = ['今', '昨', '1月', '12月', '11月', '10月']

const groupedRecords = computed(() => {
  let records = recordStore.records
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    records = records.filter(r => 
      r.personName?.toLowerCase().includes(query) ||
      r.summary?.toLowerCase().includes(query)
    )
  }
  
  const grouped = {}
  records.forEach(record => {
    const date = new Date(record.timestamp).toLocaleDateString('zh-CN')
    if (!grouped[date]) {
      grouped[date] = []
    }
    grouped[date].push(record)
  })
  return grouped
})

const formatDateRange = computed(() => ({
  start: dateRange.value.start ? new Date(dateRange.value.start).toLocaleDateString('zh-CN') : null,
  end: dateRange.value.end ? new Date(dateRange.value.end).toLocaleDateString('zh-CN') : null
}))

function setFilter(value) {
  activeFilter.value = value
  const now = new Date()
  let start, end
  
  if (value === 'week') {
    start = new Date(now.setDate(now.getDate() - 7))
    end = new Date()
  } else if (value === 'month') {
    start = new Date(now.setMonth(now.getMonth() - 1))
    end = new Date()
  } else {
    start = null
    end = null
  }
  
  recordStore.fetchRecords(start, end)
}

function setDateRange(range) {
  dateRange.value = range
  showDatePicker.value = false
  recordStore.fetchRecords(range.start, range.end)
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)
  
  if (date.toDateString() === today.toDateString()) return '今天'
  if (date.toDateString() === yesterday.toDateString()) return '昨天'
  return date.toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' })
}

function goToPerson(personId) {
  if (personId) {
    router.push(`/person/${personId}`)
  }
}

function scrollTo(month) {
  scrollToMonth.value = month
}

onMounted(() => {
  recordStore.fetchRecords()
})
</script>

<style scoped>
.timeline-page {
  background: var(--bg);
  min-height: 100vh;
}

.date-filter {
  background: var(--bg);
  padding: 8px 20px 16px;
  display: flex;
  gap: 8px;
  align-items: center;
}

.date-filter-btn {
  padding: 10px 16px;
  background: var(--bg-secondary);
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.date-filter-btn.active {
  background: var(--accent);
  color: white;
}

.date-filter-custom {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.date-sep {
  color: var(--text-tertiary);
}

.date-picker-btn {
  padding: 8px 12px;
  background: var(--bg-secondary);
  border: none;
  border-radius: 12px;
  font-size: 13px;
  color: var(--text);
  cursor: pointer;
  transition: all 0.2s ease;
}

.date-picker-btn:active {
  transform: scale(0.98);
}

.timeline-container {
  position: relative;
  display: flex;
}

.timeline-content {
  flex: 1;
}

.timeline-scroller {
  position: fixed;
  right: 8px;
  top: 200px;
  width: 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 100;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 14px;
  padding: 10px 0;
  box-shadow: var(--shadow-md);
}

.scroller-item {
  font-size: 10px;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.scroller-item.active {
  background: var(--accent);
  color: white;
}

.scroller-track {
  width: 2px;
  flex: 1;
  background: var(--separator);
  border-radius: 1px;
  margin: 6px 0;
}

.date-section {
  padding: 20px 20px 12px;
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  letter-spacing: -0.01em;
}

.empty-state {
  padding: 60px 40px;
  text-align: center;
}

.empty-icon {
  color: var(--text-tertiary);
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-text {
  font-size: 17px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.empty-hint {
  font-size: 14px;
  color: var(--text-tertiary);
}
</style>
