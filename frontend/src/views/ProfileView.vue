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
        <div class="todo-header-left">
          <span class="todo-title">待办事项</span>
          <span class="todo-count">{{ pendingTodos.length }}</span>
        </div>
        <button class="todo-add-btn" @click="showAddTodo = true">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>
      <div v-if="pendingTodos.length > 0">
        <div 
          v-for="todo in pendingTodos" 
          :key="todo.id"
          class="todo-item"
        >
          <div class="todo-checkbox" :class="{ checked: todo.completed }" @click="toggleTodo(todo.id)">
            <svg v-if="todo.completed" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
          <div class="todo-content" @click="editTodoItem(todo)">
            <div class="todo-text" :class="{ done: todo.completed }">
              {{ todo.content }}
            </div>
            <div class="todo-meta">
              <span v-if="todo.dueDate" class="todo-due" :class="{ overdue: isOverdue(todo.dueDate) }">
                {{ formatDueDate(todo.dueDate) }}
              </span>
              <span v-if="todo.personId" class="todo-person" @click.stop="goToPerson(todo.personId)">
                {{ getPersonName(todo.personId) }}
              </span>
            </div>
          </div>
          <button class="todo-delete" @click="deleteTodoItem(todo)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
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

    <div v-if="showAddTodo" class="modal-overlay" @click="showAddTodo = false">
      <div class="modal-sheet" @click.stop>
        <div class="modal-handle"></div>
        <div class="modal-header">
          <span class="modal-title">{{ editingTodo ? '编辑待办' : '新增待办' }}</span>
          <button class="modal-close" @click="cancelTodoEdit">取消</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">内容 *</label>
            <input type="text" class="form-input" v-model="todoForm.content" placeholder="待办内容">
          </div>
          <div class="form-group">
            <label class="form-label">截止日期</label>
            <input type="date" class="form-input" v-model="todoForm.dueDate">
          </div>
          <div class="form-group">
            <label class="form-label">关联人脉</label>
            <select class="form-input" v-model="todoForm.personId">
              <option :value="null">无</option>
              <option v-for="person in personStore.persons" :key="person.id" :value="person.id">
                {{ person.name }}
              </option>
            </select>
          </div>
          <div class="form-actions">
            <button v-if="editingTodo" class="btn btn-danger" @click="deleteTodoConfirm">删除</button>
            <button class="btn btn-primary" :class="{ 'btn-full': !editingTodo }" @click="saveTodo">保存</button>
          </div>
        </div>
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
const showAddTodo = ref(false)
const editingTodo = ref(null)
const todoForm = ref({
  content: '',
  dueDate: '',
  personId: null
})

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

function editTodoItem(todo) {
  editingTodo.value = todo
  todoForm.value = {
    content: todo.content,
    dueDate: todo.dueDate ? todo.dueDate.split('T')[0] : '',
    personId: todo.personId
  }
  showAddTodo.value = true
}

function cancelTodoEdit() {
  showAddTodo.value = false
  editingTodo.value = null
  todoForm.value = { content: '', dueDate: '', personId: null }
}

async function saveTodo() {
  if (!todoForm.value.content.trim()) {
    alert('请输入待办内容')
    return
  }
  
  const data = {
    content: todoForm.value.content,
    dueDate: todoForm.value.dueDate ? new Date(todoForm.value.dueDate).toISOString() : null,
    personId: todoForm.value.personId
  }
  
  if (editingTodo.value) {
    await recordStore.updateTodo(editingTodo.value.id, data)
  } else {
    await recordStore.createTodo(data)
  }
  
  cancelTodoEdit()
}

async function deleteTodoItem(todo) {
  editingTodo.value = todo
  todoForm.value = {
    content: todo.content,
    dueDate: todo.dueDate ? todo.dueDate.split('T')[0] : '',
    personId: todo.personId
  }
  showAddTodo.value = true
}

async function deleteTodoConfirm() {
  if (!editingTodo.value) return
  if (!confirm('确定要删除这个待办吗？')) return
  
  await recordStore.deleteTodo(editingTodo.value.id)
  cancelTodoEdit()
}

function isOverdue(dueDate) {
  if (!dueDate) return false
  return new Date(dueDate) < new Date()
}

function formatDueDate(dueDate) {
  if (!dueDate) return ''
  const date = new Date(dueDate)
  const today = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  
  if (date.toDateString() === today.toDateString()) return '今天'
  if (date.toDateString() === tomorrow.toDateString()) return '明天'
  
  const diff = Math.ceil((date - today) / (1000 * 60 * 60 * 24))
  if (diff < 0) return `已过期 ${Math.abs(diff)} 天`
  if (diff <= 7) return `${diff} 天后`
  
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

function getPersonName(personId) {
  const person = personStore.persons.find(p => p.id === personId)
  return person?.name || ''
}

function goToPerson(personId) {
  if (personId) {
    router.push(`/person/${personId}`)
  }
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

.todo-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.todo-add-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: var(--accent);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease;
}

.todo-add-btn:active {
  transform: scale(0.9);
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
  cursor: pointer;
  transition: all 0.2s ease;
}

.todo-checkbox.checked {
  background: var(--accent);
  border-color: var(--accent);
  color: white;
}

.todo-content {
  flex: 1;
  cursor: pointer;
}

.todo-text {
  font-size: 15px;
}

.todo-text.done {
  color: var(--text-tertiary);
  text-decoration: line-through;
}

.todo-meta {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.todo-due {
  font-size: 12px;
  color: var(--text-secondary);
  padding: 2px 6px;
  background: var(--bg-secondary);
  border-radius: 4px;
}

.todo-due.overdue {
  color: #E74C3C;
  background: rgba(231, 76, 60, 0.1);
}

.todo-person {
  font-size: 12px;
  color: var(--accent);
  cursor: pointer;
}

.todo-delete {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: var(--text-tertiary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.todo-delete:hover {
  background: rgba(231, 76, 60, 0.1);
  color: #E74C3C;
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  z-index: 2000;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.modal-sheet {
  width: 100%;
  max-width: 430px;
  background: var(--card);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  max-height: 85vh;
  overflow-y: auto;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

.modal-handle {
  width: 36px;
  height: 4px;
  background: var(--separator);
  border-radius: 2px;
  margin: 12px auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 20px 16px;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
}

.modal-close {
  font-size: 16px;
  color: var(--accent);
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.modal-body {
  padding: 0 20px 30px;
}

.form-group {
  margin-bottom: 18px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  background: var(--bg-secondary);
  border: none;
  border-radius: var(--radius-md);
  font-size: 16px;
  color: var(--text);
  outline: none;
  transition: box-shadow 0.2s ease;
}

.form-input::placeholder {
  color: var(--text-tertiary);
}

.form-input:focus {
  box-shadow: var(--shadow-md);
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.form-actions .btn {
  flex: 1;
}

.btn-full {
  width: 100%;
}
</style>
