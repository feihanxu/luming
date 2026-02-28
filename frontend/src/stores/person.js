import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const mockPersons = [
  { id: 1, name: '张总', title: '合伙人', company: '红杉资本', industry: '投资', lastContact: new Date().toISOString(), meetingCount: 12, tags: ['意大利菜', '咖啡', '红酒', '数据驱动'] },
  { id: 2, name: '李明', title: '产品总监', company: '腾讯科技', industry: '互联网', lastContact: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(), meetingCount: 5, tags: ['老同学', '游戏'] },
  { id: 3, name: '王总', title: '投资总监', company: 'IDG资本', industry: '投资', lastContact: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), meetingCount: 8, tags: ['高尔夫', '茶道'] },
  { id: 4, name: '小林', title: '高级设计师', company: '字节跳动', industry: '互联网', lastContact: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), meetingCount: 3, tags: ['设计', 'UI'] },
  { id: 5, name: '陈经理', title: '供应链经理', company: '华为', industry: '制造业', lastContact: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000).toISOString(), meetingCount: 6, tags: ['供应链', '深圳'] },
  { id: 6, name: '刘总监', title: '技术总监', company: '阿里巴巴', industry: '互联网', lastContact: new Date(Date.now() - 35 * 24 * 60 * 60 * 1000).toISOString(), meetingCount: 4, tags: ['云计算', '杭州'] }
]

export const usePersonStore = defineStore('person', () => {
  const persons = ref([...mockPersons])
  const currentPerson = ref(null)

  const recentPersons = computed(() => {
    return persons.value
      .sort((a, b) => new Date(b.lastContact) - new Date(a.lastContact))
      .slice(0, 10)
  })

  const stalePersons = computed(() => {
    const thirtyDaysAgo = new Date()
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)
    return persons.value
      .filter(p => new Date(p.lastContact) < thirtyDaysAgo)
      .sort((a, b) => new Date(a.lastContact) - new Date(b.lastContact))
  })

  async function fetchPersons() {
    try {
      const response = await fetch('/api/persons')
      const data = await response.json()
      if (data && data.length > 0) {
        persons.value = data
      }
    } catch (e) {
      console.log('Using mock persons')
    }
  }

  async function fetchPerson(id) {
    try {
      const response = await fetch(`/api/persons/${id}`)
      currentPerson.value = await response.json()
    } catch (e) {
      currentPerson.value = persons.value.find(p => p.id === parseInt(id))
    }
    return currentPerson.value
  }

  async function createPerson(data) {
    try {
      const response = await fetch('/api/persons', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      const person = await response.json()
      persons.value.push(person)
      return person
    } catch (e) {
      const newPerson = {
        ...data,
        id: Date.now(),
        lastContact: new Date().toISOString(),
        meetingCount: 0
      }
      persons.value.push(newPerson)
      return newPerson
    }
  }

  async function updatePerson(id, data) {
    try {
      const response = await fetch(`/api/persons/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      const person = await response.json()
      const index = persons.value.findIndex(p => p.id === id)
      if (index !== -1) {
        persons.value[index] = person
      }
      return person
    } catch (e) {
      const index = persons.value.findIndex(p => p.id === id)
      if (index !== -1) {
        persons.value[index] = { ...persons.value[index], ...data }
        return persons.value[index]
      }
    }
  }

  async function deletePerson(id) {
    try {
      await fetch(`/api/persons/${id}`, {
        method: 'DELETE'
      })
    } catch (e) {
      console.log('Delete locally')
    }
    const index = persons.value.findIndex(p => p.id === id)
    if (index !== -1) {
      persons.value.splice(index, 1)
    }
  }

  return {
    persons,
    currentPerson,
    recentPersons,
    stalePersons,
    fetchPersons,
    fetchPerson,
    createPerson,
    updatePerson,
    deletePerson
  }
})
