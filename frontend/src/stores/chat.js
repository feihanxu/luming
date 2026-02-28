import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const messages = ref([])
  const isLoading = ref(false)
  const currentDraft = ref(null)

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
      
      const aiMessage = {
        role: 'assistant',
        content: data.response,
        type: 'text',
        timestamp: new Date().toISOString(),
        action: data.action,
        draft: data.draft
      }
      
      messages.value.push(aiMessage)
      
      if (data.draft && data.action === 'preview') {
        currentDraft.value = data.draft
      }
      
      return data
    } finally {
      isLoading.value = false
    }
  }

  async function confirmDraft(draft) {
    isLoading.value = true
    try {
      const response = await fetch('/api/chat/confirm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(draft)
      })
      const data = await response.json()
      
      if (data.success) {
        messages.value.push({
          role: 'assistant',
          content: '保存成功啦！已帮你记录下来~',
          type: 'text',
          timestamp: new Date().toISOString(),
          record: data.record
        })
        currentDraft.value = null
      } else {
        messages.value.push({
          role: 'assistant',
          content: data.message || '保存失败，请重试',
          type: 'text',
          timestamp: new Date().toISOString()
        })
      }
      
      return data
    } finally {
      isLoading.value = false
    }
  }

  function cancelDraft() {
    currentDraft.value = null
    messages.value.push({
      role: 'assistant',
      content: '好的，已取消。还有其他要记录的吗？',
      type: 'text',
      timestamp: new Date().toISOString()
    })
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
        timestamp: new Date().toISOString(),
        action: data.action,
        draft: data.draft
      })
      
      return data
    } finally {
      isLoading.value = false
    }
  }

  function clearMessages() {
    messages.value = []
    currentDraft.value = null
  }

  return {
    messages,
    isLoading,
    currentDraft,
    sendMessage,
    confirmDraft,
    cancelDraft,
    uploadFile,
    clearMessages
  }
})
