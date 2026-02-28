import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const messages = ref([])
  const isLoading = ref(false)

  async function sendMessage(content, type = 'text') {
    messages.value.push({
      role: 'user',
      content,
      type,
      timestamp: new Date().toISOString()
    })

    isLoading.value = true
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: content, type })
      })
      const data = await response.json()
      
      messages.value.push({
        role: 'assistant',
        content: data.response,
        type: 'text',
        timestamp: new Date().toISOString(),
        record: data.record,
        avatarUpdate: data.avatarUpdate
      })
      
      return data
    } finally {
      isLoading.value = false
    }
  }

  async function uploadFile(file, description) {
    const formData = new FormData()
    formData.append('file', file)
    if (description) {
      formData.append('description', description)
    }

    isLoading.value = true
    try {
      const response = await fetch('/api/chat/upload', {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      
      messages.value.push({
        role: 'assistant',
        content: data.response,
        type: 'text',
        timestamp: new Date().toISOString()
      })
      
      return data
    } finally {
      isLoading.value = false
    }
  }

  function clearMessages() {
    messages.value = []
  }

  return {
    messages,
    isLoading,
    sendMessage,
    uploadFile,
    clearMessages
  }
})
