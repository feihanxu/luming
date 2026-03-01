import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const mockRecords = [
  {
    id: 1,
    personId: 1,
    personName: '张总',
    personTitle: '合伙人',
    personCompany: '红杉资本',
    timestamp: new Date().toISOString(),
    summary: '讨论新项目合作意向',
    location: '星巴克（国贸店）',
    topic: '项目合作、融资对接',
    todo: '下周安排团队对接'
  },
  {
    id: 2,
    personId: 2,
    personName: '李明',
    personTitle: '产品总监',
    personCompany: '腾讯科技',
    timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
    summary: '老同学聚餐',
    location: '必胜客（朝阳店）',
    topic: '聚餐、叙旧',
    note: '他最近升职了，喜欢意大利菜'
  },
  {
    id: 3,
    personId: 3,
    personName: '王总',
    personTitle: '投资总监',
    personCompany: 'IDG资本',
    timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    summary: 'A轮融资讨论',
    location: '线上会议',
    topic: '融资细节讨论',
    todo: '发送用户增长数据'
  },
  {
    id: 4,
    personId: 4,
    personName: '小林',
    personTitle: '高级设计师',
    personCompany: '字节跳动',
    timestamp: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    summary: '设计评审',
    location: '咖啡厅',
    topic: 'UI设计稿评审'
  },
  {
    id: 5,
    personId: 5,
    personName: '陈经理',
    personTitle: '供应链经理',
    personCompany: '华为',
    timestamp: new Date(Date.now() - 25 * 24 * 60 * 60 * 1000).toISOString(),
    summary: '供应链对接',
    location: '工厂',
    topic: '供应商洽谈'
  },
  {
    id: 6,
    personId: 1,
    personName: '张总',
    personTitle: '合伙人',
    personCompany: '红杉资本',
    timestamp: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
    summary: '融资讨论',
    location: '咖啡厅',
    topic: '融资细节',
    todo: '发送商业计划书'
  },
  {
    id: 7,
    personId: 6,
    personName: '刘总监',
    personTitle: '技术总监',
    personCompany: '阿里巴巴',
    timestamp: new Date(Date.now() - 35 * 24 * 60 * 60 * 1000).toISOString(),
    summary: '技术交流',
    location: '阿里园区',
    topic: '云服务合作'
  }
]

const mockTodos = [
  { id: 1, content: '下周安排团队对接（张总）', completed: false, recordDate: new Date().toISOString(), personId: 1 },
  { id: 2, content: '发送用户增长数据（王总）', completed: false, recordDate: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), personId: 3 },
  { id: 3, content: '发送商业计划书（张总）', completed: true, recordDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(), personId: 1 }
]

export const useRecordStore = defineStore('record', () => {
  const records = ref([...mockRecords])
  const todos = ref([...mockTodos])

  const recordsByDate = computed(() => {
    const grouped = {}
    records.value.forEach(record => {
      const date = new Date(record.timestamp).toLocaleDateString('zh-CN')
      if (!grouped[date]) {
        grouped[date] = []
      }
      grouped[date].push(record)
    })
    return grouped
  })

  const pendingTodos = computed(() => {
    return todos.value.filter(t => !t.completed)
  })

  const completedTodos = computed(() => {
    return todos.value.filter(t => t.completed)
  })

  async function fetchRecords(startDate, endDate) {
    const params = new URLSearchParams()
    if (startDate) params.append('start', startDate)
    if (endDate) params.append('end', endDate)
    try {
      const response = await fetch(`/api/records?${params}`)
      if (!response.ok) throw new Error('Failed to fetch records')
      const data = await response.json()
      if (data && data.length > 0) {
        records.value = data
      }
    } catch (e) {
    }
  }

  async function createRecord(data) {
    try {
      const response = await fetch('/api/records', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (!response.ok) throw new Error('Failed to create record')
      const record = await response.json()
      records.value.unshift(record)
      return record
    } catch (e) {
      const newRecord = {
        id: Date.now(),
        ...data,
        timestamp: new Date().toISOString()
      }
      records.value.unshift(newRecord)
      return newRecord
    }
  }

  async function updateRecord(id, data) {
    const index = records.value.findIndex(r => r.id === id)
    const originalRecord = index !== -1 ? { ...records.value[index] } : null
    
    try {
      const response = await fetch(`/api/records/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (!response.ok) throw new Error('Failed to update record')
      const updated = await response.json()
      if (index !== -1) {
        records.value[index] = { ...records.value[index], ...updated }
      }
      return updated
    } catch (e) {
      if (index !== -1) {
        records.value[index] = { ...records.value[index], ...data }
        return records.value[index]
      }
      throw e
    }
  }

  async function deleteRecord(id) {
    const index = records.value.findIndex(r => r.id === id)
    const deletedRecord = index !== -1 ? records.value[index] : null
    
    try {
      const response = await fetch(`/api/records/${id}`, { method: 'DELETE' })
      if (!response.ok) throw new Error('Failed to delete record')
      records.value = records.value.filter(r => r.id !== id)
    } catch (e) {
      records.value = records.value.filter(r => r.id !== id)
    }
  }

  async function fetchTodos() {
    try {
      const response = await fetch('/api/todos')
      if (!response.ok) throw new Error('Failed to fetch todos')
      const data = await response.json()
      if (data && data.length > 0) {
        todos.value = data
      }
    } catch (e) {
    }
  }

  async function toggleTodo(id) {
    const todo = todos.value.find(t => t.id === id)
    if (!todo) return
    
    const previousState = todo.completed
    todo.completed = !todo.completed
    
    try {
      const response = await fetch(`/api/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: todo.completed })
      })
      if (!response.ok) {
        todo.completed = previousState
      }
    } catch (e) {
    }
  }

  async function createTodo(data) {
    try {
      const response = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (!response.ok) throw new Error('Failed to create todo')
      const todo = await response.json()
      todos.value.push(todo)
      return todo
    } catch (e) {
      const newTodo = {
        id: Date.now(),
        ...data,
        completed: false,
        createdAt: new Date().toISOString()
      }
      todos.value.push(newTodo)
      return newTodo
    }
  }

  async function updateTodo(id, data) {
    const todo = todos.value.find(t => t.id === id)
    if (!todo) return
    
    const previousData = { ...todo }
    Object.assign(todo, data)
    
    try {
      const response = await fetch(`/api/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (!response.ok) {
        Object.assign(todo, previousData)
      }
    } catch (e) {
    }
  }

  async function deleteTodo(id) {
    const index = todos.value.findIndex(t => t.id === id)
    const deletedTodo = index !== -1 ? todos.value[index] : null
    todos.value = todos.value.filter(t => t.id !== id)
    
    try {
      const response = await fetch(`/api/todos/${id}`, { method: 'DELETE' })
      if (!response.ok && deletedTodo) {
        todos.value.splice(index, 0, deletedTodo)
      }
    } catch (e) {
    }
  }

  return {
    records,
    todos,
    recordsByDate,
    pendingTodos,
    completedTodos,
    fetchRecords,
    createRecord,
    updateRecord,
    deleteRecord,
    fetchTodos,
    toggleTodo,
    createTodo,
    updateTodo,
    deleteTodo
  }
})
