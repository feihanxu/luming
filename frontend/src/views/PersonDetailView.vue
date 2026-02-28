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
        <div class="stat-value">{{ person?.projects || 0 }}</div>
        <div class="stat-label">共同项目</div>
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
      <div class="history-date">{{ formatDateTime(record.timestamp) }}</div>
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
            <button class="btn btn-danger" @click="deletePerson">删除人脉</button>
            <button class="btn btn-secondary" @click="cancelEdit">取消</button>
            <button class="btn btn-primary" @click="saveEdit">保存</button>
          </div>
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
const editForm = ref({
  name: '',
  title: '',
  company: '',
  industry: '',
  tags: []
})
const tagsInput = ref('')

const avatarStyle = computed(() => {
  if (person.value?.avatar) {
    return { backgroundImage: `url(${person.value.avatar})`, backgroundSize: 'cover' }
  }
  return {}
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
  background: var(--bg-secondary);
  max-width: 430px;
  margin: 0 auto;
  overflow-y: auto;
  z-index: 1500;
}

.detail-header {
  background: var(--bg);
  padding: 56px 16px 16px;
  text-align: center;
  border-bottom: 0.5px solid var(--separator);
  position: relative;
}

.detail-back {
  position: absolute;
  top: 14px;
  left: 16px;
  font-size: 17px;
  color: var(--accent);
  background: none;
  border: none;
  cursor: pointer;
}

.detail-edit {
  position: absolute;
  top: 14px;
  right: 16px;
  font-size: 17px;
  color: var(--accent);
  background: none;
  border: none;
  cursor: pointer;
}

.detail-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #E0E0E0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 500;
  color: var(--text-secondary);
  margin: 0 auto 8px;
}

.detail-name {
  font-size: 20px;
  font-weight: 600;
}

.detail-meta {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.stats-card {
  background: var(--bg);
  margin: 12px 16px;
  border-radius: 12px;
  padding: 14px;
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 22px;
  font-weight: 600;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.info-card {
  background: var(--bg);
  margin: 0 16px 12px;
  border-radius: 12px;
  padding: 14px;
}

.info-title {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 10px;
}

.info-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.info-tag {
  padding: 5px 10px;
  background: var(--bg-secondary);
  border-radius: 6px;
  font-size: 13px;
  color: var(--text-secondary);
}

.info-empty {
  font-size: 14px;
  color: var(--text-tertiary);
}

.history-card {
  background: var(--bg);
  margin: 0 16px 8px;
  border-radius: 12px;
  padding: 12px;
}

.history-date {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.history-content {
  font-size: 14px;
  line-height: 1.4;
}

.history-struct {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
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
  font-size: 14px;
  color: var(--text);
}

.struct-value.todo {
  color: var(--accent);
}

.empty-state {
  padding: 40px;
  text-align: center;
  color: var(--text-tertiary);
}

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
  max-height: 80vh;
  overflow-y: auto;
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

.form-group {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.form-input {
  width: 100%;
  padding: 12px;
  background: var(--bg-secondary);
  border: none;
  border-radius: 8px;
  font-size: 16px;
  color: var(--text);
  outline: none;
}

.form-input::placeholder {
  color: var(--text-tertiary);
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.form-actions .btn {
  flex: 1;
}
</style>
