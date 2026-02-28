<template>
  <div class="chat-page">
    <div class="page-header">
      <div class="page-title">呦呦</div>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div 
        v-for="(message, index) in messages" 
        :key="index"
        class="chat-bubble fade-in"
        :class="message.role"
      >
        <template v-if="message.type === 'text'">
          {{ message.content }}
        </template>
        <template v-else-if="message.type === 'image'">
          <div class="chat-image-container">
            <img :src="message.content" alt="上传的图片" />
          </div>
          <div v-if="message.caption" class="chat-image-caption">
            {{ message.caption }}
          </div>
        </template>
        
        <div v-if="message.record" class="chat-record-card">
          <div class="chat-record-header">
            <span class="chat-record-person">{{ message.record.personName }}</span>
            <span class="chat-record-time">刚刚</span>
          </div>
          <div class="chat-record-content">
            <div v-if="message.record.location" class="chat-record-row">
              <span class="chat-record-label">地点</span>
              <span class="chat-record-value">{{ message.record.location }}</span>
            </div>
            <div v-if="message.record.topic" class="chat-record-row">
              <span class="chat-record-label">事项</span>
              <span class="chat-record-value">{{ message.record.topic }}</span>
            </div>
            <div v-if="message.record.todo" class="chat-record-row">
              <span class="chat-record-label">待办</span>
              <span class="chat-record-value todo">{{ message.record.todo }}</span>
            </div>
          </div>
        </div>

        <div v-if="message.avatarUpdate" class="chat-avatar-preview">
          <div class="chat-avatar-new">
            <span>{{ message.avatarUpdate.name?.charAt(0) }}</span>
            <div class="chat-avatar-badge">✓</div>
          </div>
          <div class="chat-avatar-info">
            <div class="chat-avatar-name">{{ message.avatarUpdate.name }}</div>
            <div class="chat-avatar-desc">头像已更新</div>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="chat-bubble ai breathing">
        <span class="typing-indicator">正在思考...</span>
      </div>
    </div>

    <div class="suggestions">
      <button 
        v-for="suggestion in suggestions" 
        :key="suggestion"
        class="suggestion-btn"
        @click="sendSuggestion(suggestion)"
      >
        {{ suggestion }}
      </button>
    </div>

    <div class="chat-input-area">
      <button class="chat-attach-btn" @click="showAttachMenu = !showAttachMenu">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </button>
      <input 
        type="text" 
        class="chat-input" 
        placeholder="说说你今天见了谁..."
        v-model="inputText"
        @keypress.enter="sendMessage"
      />
      <button class="chat-send" @click="sendMessage">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </div>

    <div v-if="showAttachMenu" class="attach-menu">
      <div class="attach-menu-item" @click="selectFile('image')">
        <div class="attach-icon photo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
        <span>照片</span>
      </div>
      <div class="attach-menu-item" @click="selectFile('audio')">
        <div class="attach-icon audio">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
        </div>
        <span>录音</span>
      </div>
    </div>

    <input 
      ref="fileInput"
      type="file" 
      :accept="fileAccept"
      style="display: none"
      @change="handleFileSelect"
    />
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { useChatStore } from '../stores/chat'

const chatStore = useChatStore()

const messagesContainer = ref(null)
const fileInput = ref(null)
const inputText = ref('')
const showAttachMenu = ref(false)
const fileType = ref('image')

const messages = computed(() => chatStore.messages)
const isLoading = computed(() => chatStore.isLoading)

const suggestions = [
  '今天见了谁？',
  '发照片记录头像',
  '好久没联系谁了'
]

const fileAccept = computed(() => 
  fileType.value === 'image' ? 'image/*' : 'audio/*'
)

async function sendMessage() {
  if (!inputText.value.trim()) return
  
  const text = inputText.value
  inputText.value = ''
  
  await chatStore.sendMessage(text)
  scrollToBottom()
}

function sendSuggestion(suggestion) {
  inputText.value = suggestion
  sendMessage()
}

function selectFile(type) {
  fileType.value = type
  showAttachMenu.value = false
  fileInput.value?.click()
}

async function handleFileSelect(event) {
  const file = event.target.files?.[0]
  if (!file) return
  
  await chatStore.uploadFile(file, inputText.value)
  inputText.value = ''
  scrollToBottom()
  event.target.value = ''
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

onMounted(() => {
  if (messages.value.length === 0) {
    chatStore.messages.push({
      role: 'assistant',
      content: '你好呀！我是呦呦，你的人脉小助手。',
      type: 'text',
      timestamp: new Date().toISOString()
    })
    chatStore.messages.push({
      role: 'assistant',
      content: '你可以告诉我今天见了谁、聊了什么，也可以发照片让我帮你记录人物头像。',
      type: 'text',
      timestamp: new Date().toISOString()
    })
  }
})
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 104px);
  position: relative;
  padding-bottom: 80px;
  background: var(--bg);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  padding-bottom: 100px;
}

.chat-bubble {
  max-width: 80%;
  padding: 14px 18px;
  border-radius: 20px;
  margin-bottom: 12px;
  font-size: 16px;
  line-height: 1.5;
  word-wrap: break-word;
}

.chat-bubble.user {
  background: var(--accent-gradient);
  color: white;
  margin-left: auto;
  border-bottom-right-radius: 6px;
  box-shadow: var(--shadow-sm);
}

.chat-bubble.ai {
  background: var(--card);
  color: var(--text);
  border-bottom-left-radius: 6px;
  box-shadow: var(--shadow-sm);
}

.typing-indicator {
  color: var(--text-secondary);
}

.chat-image-container {
  border-radius: 14px;
  overflow: hidden;
  margin-bottom: 8px;
}

.chat-image-container img {
  max-width: 200px;
  max-height: 150px;
  object-fit: cover;
}

.chat-image-caption {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.85);
  margin-top: 6px;
}

.chat-record-card {
  max-width: 85%;
  background: var(--bg);
  border-radius: 14px;
  margin-top: 10px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.chat-record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid var(--separator);
}

.chat-record-person {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
}

.chat-record-time {
  font-size: 13px;
  color: var(--text-tertiary);
  padding: 4px 10px;
  background: var(--bg-secondary);
  border-radius: 20px;
}

.chat-record-content {
  padding: 14px 16px;
}

.chat-record-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 8px;
}

.chat-record-row:last-child {
  margin-bottom: 0;
}

.chat-record-label {
  font-size: 13px;
  color: var(--text-tertiary);
  min-width: 40px;
  font-weight: 500;
}

.chat-record-value {
  font-size: 15px;
  color: var(--text);
}

.chat-record-value.todo {
  color: var(--accent);
  font-weight: 500;
}

.chat-avatar-preview {
  display: flex;
  align-items: center;
  gap: 14px;
  max-width: 85%;
  background: var(--bg);
  border-radius: 14px;
  padding: 14px 16px;
  margin-top: 10px;
  box-shadow: var(--shadow-sm);
}

.chat-avatar-new {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--accent-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  color: white;
  position: relative;
}

.chat-avatar-badge {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 20px;
  height: 20px;
  background: var(--green);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: white;
  border: 2px solid white;
}

.chat-avatar-info {
  flex: 1;
}

.chat-avatar-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
}

.chat-avatar-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 3px;
}

.suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 16px 20px;
  padding-bottom: 80px;
}

.suggestion-btn {
  padding: 12px 18px;
  background: var(--card);
  border: none;
  border-radius: 20px;
  font-size: 15px;
  color: var(--text);
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.suggestion-btn:active {
  transform: scale(0.98);
  box-shadow: var(--shadow-md);
}

.chat-input-area {
  position: fixed;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 430px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 12px 20px;
  display: flex;
  gap: 12px;
  align-items: center;
  z-index: 100;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.04);
}

.chat-attach-btn {
  width: 40px;
  height: 40px;
  background: var(--bg-secondary);
  border: none;
  border-radius: 50%;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  transition: all 0.2s ease;
}

.chat-attach-btn:active {
  background: var(--accent-light);
  color: var(--accent);
}

.chat-input {
  flex: 1;
  background: var(--bg-secondary);
  border: none;
  border-radius: 24px;
  padding: 12px 18px;
  font-size: 16px;
  outline: none;
  min-height: 44px;
  line-height: 20px;
}

.chat-input::placeholder {
  color: var(--text-tertiary);
}

.chat-send {
  width: 44px;
  height: 44px;
  background: var(--accent-gradient);
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.chat-send:active {
  transform: scale(0.95);
}

.attach-menu {
  position: fixed;
  bottom: 140px;
  left: 50%;
  transform: translateX(-50%);
  max-width: 430px;
  width: calc(100% - 40px);
  background: var(--card);
  border-radius: var(--radius-lg);
  padding: 12px;
  box-shadow: var(--shadow-lg);
  z-index: 200;
  display: flex;
  gap: 12px;
}

.attach-menu-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 20px;
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: background 0.2s ease;
}

.attach-menu-item:active {
  background: var(--bg-secondary);
}

.attach-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.attach-icon.photo {
  background: var(--accent-light);
  color: var(--accent);
}

.attach-icon.audio {
  background: rgba(212, 165, 116, 0.15);
  color: var(--orange);
}

.attach-menu-item span {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}
</style>
