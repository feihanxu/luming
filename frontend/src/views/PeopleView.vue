<template>
  <div class="people-page">
    <div class="page-header">
      <div class="page-title">人脉</div>
      <div class="header-action" @click="showAddModal = true">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </div>
    </div>

    <div class="search-bar">
      <input type="text" class="search-input" placeholder="搜索" v-model="searchQuery">
    </div>

    <div v-if="recentPersons.length > 0">
      <div class="section-label">最近联系</div>
      <PersonCard 
        v-for="person in filteredRecentPersons" 
        :key="person.id" 
        :person="person"
        @click="goToPerson(person.id)"
      />
    </div>

    <div v-if="stalePersons.length > 0">
      <div class="section-label">久未联系</div>
      <PersonCard 
        v-for="person in filteredStalePersons" 
        :key="person.id" 
        :person="person"
        @click="goToPerson(person.id)"
      />
    </div>

    <div v-if="filteredPersons.length === 0" class="empty-state">
      暂无人脉记录
    </div>

    <div v-if="showAddModal" class="modal-overlay" @click="showAddModal = false">
      <div class="modal-sheet" @click.stop>
        <div class="modal-header">
          <span class="modal-title">新增人脉</span>
          <button class="modal-close" @click="showAddModal = false">取消</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">姓名 *</label>
            <input type="text" class="form-input" v-model="newPerson.name" placeholder="请输入姓名">
          </div>
          <div class="form-group">
            <label class="form-label">职位</label>
            <input type="text" class="form-input" v-model="newPerson.title" placeholder="如：产品总监">
          </div>
          <div class="form-group">
            <label class="form-label">公司</label>
            <input type="text" class="form-input" v-model="newPerson.company" placeholder="如：腾讯科技">
          </div>
          <div class="form-group">
            <label class="form-label">行业</label>
            <input type="text" class="form-input" v-model="newPerson.industry" placeholder="如：互联网">
          </div>
          <div class="form-group">
            <label class="form-label">偏好标签</label>
            <input type="text" class="form-input" v-model="tagsInput" placeholder="用逗号分隔，如：咖啡, 红酒, 高尔夫">
          </div>
          <button class="btn btn-primary btn-full" @click="addPerson">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePersonStore } from '../stores/person'
import PersonCard from '../components/PersonCard.vue'

const router = useRouter()
const personStore = usePersonStore()

const searchQuery = ref('')
const showAddModal = ref(false)
const newPerson = ref({
  name: '',
  title: '',
  company: '',
  industry: '',
  tags: []
})
const tagsInput = ref('')

const recentPersons = computed(() => personStore.recentPersons)
const stalePersons = computed(() => personStore.stalePersons)

const filteredRecentPersons = computed(() => {
  if (!searchQuery.value) return recentPersons.value
  const query = searchQuery.value.toLowerCase()
  return recentPersons.value.filter(p => 
    p.name.toLowerCase().includes(query) ||
    p.company?.toLowerCase().includes(query) ||
    p.title?.toLowerCase().includes(query) ||
    p.tags?.some(t => t.toLowerCase().includes(query))
  )
})

const filteredStalePersons = computed(() => {
  if (!searchQuery.value) return stalePersons.value
  const query = searchQuery.value.toLowerCase()
  return stalePersons.value.filter(p => 
    p.name.toLowerCase().includes(query) ||
    p.company?.toLowerCase().includes(query) ||
    p.title?.toLowerCase().includes(query) ||
    p.tags?.some(t => t.toLowerCase().includes(query))
  )
})

const filteredPersons = computed(() => 
  [...filteredRecentPersons.value, ...filteredStalePersons.value]
)

function goToPerson(id) {
  router.push(`/person/${id}`)
}

async function addPerson() {
  if (!newPerson.value.name.trim()) {
    alert('请输入姓名')
    return
  }
  
  const tags = tagsInput.value
    .split(/[,，]/)
    .map(t => t.trim())
    .filter(t => t)
  
  const person = {
    ...newPerson.value,
    tags
  }
  
  await personStore.createPerson(person)
  
  newPerson.value = {
    name: '',
    title: '',
    company: '',
    industry: '',
    tags: []
  }
  tagsInput.value = ''
  showAddModal.value = false
}

onMounted(() => {
  personStore.fetchPersons()
})
</script>

<style scoped>
.people-page {
  background: var(--bg-secondary);
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

.form-input:focus {
  background: var(--bg-secondary);
}

.btn-full {
  width: 100%;
  margin-top: 8px;
}
</style>
