<template>
  <div class="profile-page">
    <div class="page-header">
      <div class="page-title">我的</div>
      <div class="header-action" @click="goToSettings">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="3"></circle>
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
        </svg>
      </div>
    </div>

    <div class="profile-header">
      <div class="profile-avatar">{{ userInitial }}</div>
      <div class="profile-name">{{ userName }}</div>
      <div class="profile-desc">记录每一次相遇的温度</div>
      <div class="profile-stats">
        <div class="profile-stat">
          <div class="profile-stat-value">{{ stats.persons }}</div>
          <div class="profile-stat-label">人脉</div>
        </div>
        <div class="profile-stat">
          <div class="profile-stat-value">{{ stats.records }}</div>
          <div class="profile-stat-label">记录</div>
        </div>
        <div class="profile-stat">
          <div class="profile-stat-value">{{ stats.todos }}</div>
          <div class="profile-stat-label">待办</div>
        </div>
      </div>
    </div>

    <div class="todo-section">
      <div class="todo-header">
        <span class="todo-title">待办事项</span>
        <span class="todo-count">{{ pendingTodos.length }}</span>
      </div>
      <div v-if="pendingTodos.length > 0">
        <div 
          v-for="todo in pendingTodos" 
          :key="todo.id"
          class="todo-item"
          @click="toggleTodo(todo.id)"
        >
          <div class="todo-checkbox" :class="{ checked: todo.completed }">
            {{ todo.completed ? '✓' : '' }}
          </div>
          <div class="todo-content">
            <div class="todo-text" :class="{ done: todo.completed }">
              {{ todo.content }}
            </div>
            <div class="todo-meta">来自 {{ formatDate(todo.recordDate) }} 记录</div>
          </div>
        </div>
      </div>
      <div v-else class="todo-empty">
        暂无待办事项
      </div>
    </div>

    <div class="menu-section">
      <div class="menu-item" @click="showPreferences = true">
        <span class="menu-label">我的偏好</span>
        <span class="menu-arrow">›</span>
      </div>
      <div class="menu-item" @click="exportData">
        <span class="menu-label">数据备份</span>
        <span class="menu-arrow">›</span>
      </div>
      <div class="menu-item" @click="showHelp = true">
        <span class="menu-label">帮助与反馈</span>
        <span class="menu-arrow">›</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRecordStore } from '../stores/record'
import { usePersonStore } from '../stores/person'

const router = useRouter()
const recordStore = useRecordStore()
const personStore = usePersonStore()

const userName = ref('用户')
const showPreferences = ref(false)
const showHelp = ref(false)

const userInitial = computed(() => userName.value.charAt(0))

const stats = computed(() => ({
  persons: personStore.persons.length,
  records: recordStore.records.length,
  todos: recordStore.pendingTodos.length
}))

const pendingTodos = computed(() => recordStore.pendingTodos)

function goToSettings() {
  router.push('/settings')
}

async function toggleTodo(id) {
  await recordStore.toggleTodo(id)
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' })
}

async function exportData() {
  const data = {
    persons: personStore.persons,
    records: recordStore.records,
    todos: recordStore.todos,
    exportDate: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `luming-backup-${new Date().toISOString().split('T')[0]}.json`
  a.click()
  URL.revokeObjectURL(url)
}

onMounted(() => {
  recordStore.fetchTodos()
  personStore.fetchPersons()
  recordStore.fetchRecords()
})
</script>

<style scoped>
.profile-page {
  background: var(--bg-secondary);
}

.profile-header {
  background: var(--bg);
  padding: 20px 16px;
  text-align: center;
  border-bottom: 0.5px solid var(--separator);
}

.profile-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 500;
  color: white;
  margin: 0 auto 12px;
}

.profile-name {
  font-size: 22px;
  font-weight: 600;
}

.profile-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.profile-stats {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-top: 16px;
}

.profile-stat {
  text-align: center;
}

.profile-stat-value {
  font-size: 20px;
  font-weight: 600;
}

.profile-stat-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.todo-section {
  background: var(--bg);
  margin: 16px;
  border-radius: 12px;
  overflow: hidden;
}

.todo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 0.5px solid var(--separator);
}

.todo-title {
  font-size: 15px;
  font-weight: 500;
}

.todo-count {
  font-size: 13px;
  color: var(--accent);
  background: var(--accent-light);
  padding: 2px 8px;
  border-radius: 10px;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
}

.todo-item:active {
  background: var(--bg-secondary);
}

.todo-item + .todo-item {
  border-top: 0.5px solid var(--separator);
}

.todo-checkbox {
  width: 22px;
  height: 22px;
  border: 2px solid var(--separator);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.todo-checkbox.checked {
  background: var(--green);
  border-color: var(--green);
  color: white;
  font-size: 12px;
}

.todo-content {
  flex: 1;
}

.todo-text {
  font-size: 15px;
}

.todo-text.done {
  color: var(--text-tertiary);
  text-decoration: line-through;
}

.todo-meta {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 2px;
}

.todo-empty {
  padding: 20px;
  text-align: center;
  color: var(--text-tertiary);
  font-size: 14px;
}

.menu-section {
  background: var(--bg);
  margin: 16px;
  border-radius: 12px;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  cursor: pointer;
}

.menu-item:active {
  background: var(--bg-secondary);
}

.menu-item + .menu-item {
  border-top: 0.5px solid var(--separator);
}

.menu-label {
  flex: 1;
  font-size: 17px;
}

.menu-arrow {
  color: var(--text-tertiary);
  font-size: 14px;
  margin-left: 4px;
}
</style>
