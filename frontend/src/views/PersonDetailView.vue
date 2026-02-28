<template>
  <div class="detail-page">
    <div class="detail-header">
      <button class="detail-back" @click="goBack">← 返回</button>
      <button class="detail-edit" @click="startEdit">编辑</button>
      <div class="detail-avatar" :style="avatarStyle">
        {{ person?.name?.charAt(0) }}
      </div>
      <div class="detail-name">{{ person?.name }}</div>
      <div class="detail-meta">{{ person?.title }} · {{ person?.company }}</div>
    </div>

    <div class="stats-card">
      <div class="stat-item">
        <div class="stat-value">{{ person?.meetingCount || 0 }}</div>
        <div class="stat-label">见面次数</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ daysSinceLastContact }}</div>
        <div class="stat-label">天前见面</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ records.length }}</div>
        <div class="stat-label">互动记录</div>
      </div>
    </div>

    <div class="info-card">
      <div class="info-title">偏好标签</div>
      <div class="info-tags">
        <span v-for="tag in person?.tags" :key="tag" class="info-tag">
          {{ tag }}
        </span>
      </div>
      <div v-if="!person?.tags?.length" class="info-empty">暂无偏好标签</div>
    </div>

    <div class="section-label">见面记录</div>

    <div 
      v-for="record in records" 
      :key="record.id"
      class="history-card"
    >
      <div class="history-header">
        <div class="history-date">{{ formatDateTime(record.timestamp) }}</div>
        <div class="history-actions">
          <button class="action-btn" @click="editRecord(record)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button class="action-btn danger" @click="confirmDeleteRecord(record)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>
      </div>
      <div class="history-content">{{ record.summary }}</div>
      <div class="history-struct">
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
      </div>
    </div>

    <div v-if="records.length === 0" class="empty-state">
      暂无见面记录
    </div>

    <div v-if="isEditing" class="modal-overlay" @click="cancelEdit">
      <div class="modal-sheet" @click.stop>
        <div class="modal-handle"></div>
        <div class="modal-header">
          <span class="modal-title">编辑人脉</span>
          <button class="modal-close" @click="cancelEdit">取消</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">姓名 *</label>
            <input type="text" class="form-input" v-model="editForm.name" placeholder="请输入姓名">
          </div>
          <div class="form-group">
            <label class="form-label">职位</label>
            <input type="text" class="form-input" v-model="editForm.title" placeholder="如：产品总监">
          </div>
          <div class="form-group">
            <label class="form-label">公司</label>
            <input type="text" class="form-input" v-model="editForm.company" placeholder="如：腾讯科技">
          </div>
          <div class="form-group">
            <label class="form-label">行业</label>
            <input type="text" class="form-input" v-model="editForm.industry" placeholder="如：互联网">
          </div>
          <div class="form-group">
            <label class="form-label">偏好标签</label>
            <input type="text" class="form-input" v-model="tagsInput" placeholder="用逗号分隔，如：咖啡, 红酒, 高尔夫">
          </div>
          <div class="form-actions">
            <button class="btn btn-danger" @click="deletePerson">删除</button>
            <button class="btn btn-primary" @click="saveEdit">保存</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isEditingRecord" class="modal-overlay" @click="cancelEditRecord">
      <div class="modal-sheet" @click.stop>
        <div class="modal-handle"></div>
        <div class="modal-header">
          <span class="modal-title">编辑记录</span>
          <button class="modal-close" @click="cancelEditRecord">取消</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">摘要</label>
            <textarea class="form-textarea" v-model="recordEditForm.summary" placeholder="见面摘要" rows="2"></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">地点</label>
            <input type="text" class="form-input" v-model="recordEditForm.location" placeholder="见面地点">
          </div>
          <div class="form-group">
            <label class="form-label">事项</label>
            <input type="text" class="form-input" v-model="recordEditForm.topic" placeholder="讨论事项">
          </div>
          <div class="form-group">
            <label class="form-label">待办</label>
            <input type="text" class="form-input" v-model="recordEditForm.todo" placeholder="后续待办">
          </div>
          <div class="form-group">
            <label class="form-label">备注</label>
            <textarea class="form-textarea" v-model="recordEditForm.note" placeholder="其他备注" rows="2"></textarea>
          </div>
          <button class="btn btn-primary btn-full" @click="saveRecordEdit">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePersonStore } from '../stores/person'
import { useRecordStore } from '../stores/record'

const route = useRoute()
const router = useRouter()
const personStore = usePersonStore()
const recordStore = useRecordStore()

const person = ref(null)
const records = ref([])
const isEditing = ref(false)
const isEditingRecord = ref(false)
const editingRecordId = ref(null)
const editForm = ref({
  name: '',
  title: '',
  company: '',
  industry: '',
  tags: []
})
const recordEditForm = ref({
  summary: '',
  location: '',
  topic: '',
  todo: '',
  note: ''
})
const tagsInput = ref('')

const avatarColors = [
  'linear-gradient(135deg, #7C9A92 0%, #9DB5AD 100%)',
  'linear-gradient(135deg, #A390C4 0%, #C4B5D9 100%)',
  'linear-gradient(135deg, #7BA3C9 0%, #9DBED9 100%)',
  'linear-gradient(135deg, #D4A574 0%, #E5C4A4 100%)',
  'linear-gradient(135deg, #C9707D 0%, #D999A3 100%)'
]

const avatarStyle = computed(() => {
  if (person.value?.avatar) {
    return { backgroundImage: `url(${person.value.avatar})`, backgroundSize: 'cover' }
  }
  const colorIndex = (person.value?.name?.charCodeAt(0) || 0) % avatarColors.length
  return { background: avatarColors[colorIndex] }
})

const daysSinceLastContact = computed(() => {
  if (!person.value?.lastContact) return '-'
  const last = new Date(person.value.lastContact)
  const now = new Date()
  return Math.floor((now - last) / (1000 * 60 * 60 * 24))
})

function goBack() {
  router.back()
}

function startEdit() {
  isEditing.value = true
  editForm.value = {
    name: person.value?.name || '',
    title: person.value?.title || '',
    company: person.value?.company || '',
    industry: person.value?.industry || '',
    tags: person.value?.tags || []
  }
  tagsInput.value = (person.value?.tags || []).join(', ')
}

function cancelEdit() {
  isEditing.value = false
}

async function saveEdit() {
  if (!editForm.value.name.trim()) {
    alert('请输入姓名')
    return
  }
  
  const tags = tagsInput.value
    .split(/[,，]/)
    .map(t => t.trim())
    .filter(t => t)
  
  await personStore.updatePerson(person.value.id, {
    ...editForm.value,
    tags
  })
  
  person.value = {
    ...person.value,
    ...editForm.value,
    tags
  }
  isEditing.value = false
}

async function deletePerson() {
  if (!confirm(`确定要删除「${person.value?.name}」吗？相关记录也会被删除。`)) {
    return
  }
  
  await personStore.deletePerson(person.value.id)
  router.back()
}

function editRecord(record) {
  isEditingRecord.value = true
  editingRecordId.value = record.id
  recordEditForm.value = {
    summary: record.summary || '',
    location: record.location || '',
    topic: record.topic || '',
    todo: record.todo || '',
    note: record.note || ''
  }
}

function cancelEditRecord() {
  isEditingRecord.value = false
  editingRecordId.value = null
}

async function saveRecordEdit() {
  if (!editingRecordId.value) return
  
  await recordStore.updateRecord(editingRecordId.value, recordEditForm.value)
  
  const index = records.value.findIndex(r => r.id === editingRecordId.value)
  if (index !== -1) {
    records.value[index] = { ...records.value[index], ...recordEditForm.value }
  }
  
  isEditingRecord.value = false
  editingRecordId.value = null
}

async function confirmDeleteRecord(record) {
  if (!confirm('确定要删除这条记录吗？')) {
    return
  }
  
  await recordStore.deleteRecord(record.id)
  records.value = records.value.filter(r => r.id !== record.id)
}

function formatDateTime(timestamp) {
  return new Date(timestamp).toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  const id = route.params.id
  person.value = await personStore.fetchPerson(id)
  
  const allRecords = recordStore.records.filter(r => r.personId === parseInt(id))
  records.value = allRecords.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
})
</script>

<style scoped>
.detail-page {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bg);
  max-width: 430px;
  margin: 0 auto;
  overflow-y: auto;
  z-index: 1500;
}

.detail-header {
  background: var(--bg);
  padding: 56px 20px 24px;
  text-align: center;
  position: relative;
}

.detail-back {
  position: absolute;
  top: 16px;
  left: 16px;
  font-size: 16px;
  color: var(--accent);
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.detail-edit {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 16px;
  color: var(--accent);
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.detail-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  font-weight: 600;
  color: white;
  margin: 0 auto 12px;
}

.detail-name {
  font-size: 22px;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.detail-meta {
  font-size: 15px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.stats-card {
  background: var(--card);
  margin: 0 16px 16px;
  border-radius: var(--radius-md);
  padding: 20px;
  display: flex;
  justify-content: space-around;
  box-shadow: var(--shadow-sm);
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--accent);
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.info-card {
  background: var(--card);
  margin: 0 16px 16px;
  border-radius: var(--radius-md);
  padding: 18px;
  box-shadow: var(--shadow-sm);
}

.info-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.info-tag {
  padding: 6px 12px;
  background: var(--accent-light);
  color: var(--accent);
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.info-empty {
  font-size: 14px;
  color: var(--text-tertiary);
}

.section-label {
  padding: 20px 20px 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.history-card {
  background: var(--card);
  margin: 0 16px 12px;
  border-radius: var(--radius-md);
  padding: 16px;
  box-shadow: var(--shadow-sm);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.history-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.action-btn:active {
  transform: scale(0.9);
}

.action-btn.danger {
  color: #E74C3C;
}

.action-btn.danger:active {
  background: rgba(231, 76, 60, 0.1);
}

.history-date {
  font-size: 13px;
  color: var(--text-tertiary);
  margin-bottom: 8px;
}

.history-content {
  font-size: 15px;
  line-height: 1.5;
  color: var(--text);
}

.history-struct {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.struct-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.struct-label {
  font-size: 13px;
  color: var(--text-tertiary);
  min-width: 48px;
  font-weight: 500;
}

.struct-value {
  font-size: 14px;
  color: var(--text);
}

.struct-value.todo {
  color: var(--accent);
  font-weight: 500;
}

.empty-state {
  padding: 60px 40px;
  text-align: center;
  color: var(--text-tertiary);
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

.form-textarea {
  width: 100%;
  padding: 14px 16px;
  background: var(--bg-secondary);
  border: none;
  border-radius: var(--radius-md);
  font-size: 16px;
  color: var(--text);
  outline: none;
  transition: box-shadow 0.2s ease;
  resize: none;
  font-family: inherit;
}

.form-textarea::placeholder {
  color: var(--text-tertiary);
}

.form-textarea:focus {
  box-shadow: var(--shadow-md);
}

.form-divider {
  height: 1px;
  background: var(--separator);
  margin: 20px 0;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.form-actions .btn {
  flex: 1;
}
</style>
