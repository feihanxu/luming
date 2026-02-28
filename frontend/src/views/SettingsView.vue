<template>
  <div class="settings-page">
    <div class="page-header">
      <button class="detail-back" @click="goBack">← 返回</button>
      <div class="page-title">设置</div>
    </div>

    <div class="section-label">外观</div>
    <div class="theme-options">
      <div 
        v-for="theme in themes" 
        :key="theme.value"
        class="theme-option"
        :class="{ active: currentTheme === theme.value }"
        @click="setTheme(theme.value)"
      >
        <div class="theme-preview" :class="theme.value"></div>
        <span class="theme-name">{{ theme.label }}</span>
      </div>
    </div>

    <div class="menu-section">
      <div class="menu-item" @click="showModelSelector = true">
        <span class="menu-label">AI 模型</span>
        <span class="menu-value">{{ currentModel }}</span>
        <span class="menu-arrow">›</span>
      </div>
      <div class="menu-item" @click="showSpeechSelector = true">
        <span class="menu-label">语音识别</span>
        <span class="menu-value">{{ currentSpeech }}</span>
        <span class="menu-arrow">›</span>
      </div>
    </div>

    <div class="menu-section">
      <div class="menu-item" @click="exportData">
        <span class="menu-label">导出数据</span>
        <span class="menu-arrow">›</span>
      </div>
      <div class="menu-item" @click="triggerImport">
        <span class="menu-label">导入数据</span>
        <span class="menu-arrow">›</span>
      </div>
      <input ref="fileInput" type="file" accept=".json" style="display: none" @change="importData">
    </div>

    <div class="menu-section">
      <div class="menu-item" @click="showPrivacy = true">
        <span class="menu-label">隐私设置</span>
        <span class="menu-arrow">›</span>
      </div>
      <div class="menu-item">
        <span class="menu-label">关于鹿鸣</span>
        <span class="menu-value">v1.0.0</span>
        <span class="menu-arrow">›</span>
      </div>
    </div>

    <div class="api-key-section">
      <div class="section-label">API 设置</div>
      <div class="api-key-input">
        <input 
          type="password" 
          v-model="apiKey" 
          placeholder="请输入 API Key"
          class="search-input"
        >
        <button class="btn btn-primary" @click="saveApiKey">保存</button>
      </div>
      <div class="api-url-input">
        <input 
          type="text" 
          v-model="apiUrl" 
          placeholder="API 地址（可选）"
          class="search-input"
        >
      </div>
    </div>

    <div v-if="showModelSelector" class="modal-overlay" @click="showModelSelector = false">
      <div class="modal-sheet" @click.stop>
        <div class="modal-header">
          <span class="modal-title">选择 AI 模型</span>
          <button class="modal-close" @click="showModelSelector = false">完成</button>
        </div>
        <div class="section-label-model">选择你要使用的 AI 模型</div>
        <div class="model-selector">
          <div 
            v-for="model in aiModels" 
            :key="model.value"
            class="model-option"
            :class="{ active: currentModel === model.value }"
            @click="selectModel(model.value)"
          >
            {{ model.label }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const fileInput = ref(null)

const themes = [
  { label: '浅色', value: 'light' },
  { label: '深色', value: 'dark' },
  { label: '跟随系统', value: 'system' },
  { label: '护眼', value: 'warm' }
]

const aiModels = [
  { label: 'GLM-4', value: 'glm-4', placeholder: '智谱AI GLM-4', url: 'https://open.bigmodel.cn/api/paas/v4/chat/completions' },
  { label: 'GPT-4o', value: 'gpt-4o', placeholder: 'OpenAI GPT-4o', url: 'https://api.openai.com/v1/chat/completions' },
  { label: 'Claude 3.5 Sonnet', value: 'claude-3.5-sonnet', placeholder: 'Anthropic Claude 3.5 Sonnet', url: 'https://api.anthropic.com/v1/messages' },
  { label: 'DeepSeek', value: 'deepseek', placeholder: 'DeepSeek API', url: 'https://api.deepseek.com/v1/chat/completions' },
  { label: '通义千问', value: 'qwen', placeholder: '阿里云通义千问', url: 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' },
  { label: '文心一言', value: 'ernie', placeholder: '百度文心一言', url: 'https://aip.baidubce.com/rpc/2.0/ernie-bot-4' },
  { label: 'Moonshot', value: 'moonshot', placeholder: 'Moonshot AI', url: 'https://api.moonshot.ai/v1/chat/completions' },
  { label: '自定义', value: 'custom', placeholder: '自定义 API 地址', url: '' }
]

const speechServices = [
  { label: '讯飞', value: 'xunfei' },
  { label: '阿里云', value: 'aliyun' },
  { label: '腾讯云', value: 'tencent' },
]

const currentTheme = ref('light')
const currentModel = ref('glm-4')
const currentModelConfig = ref({})
const currentSpeech = ref('xunfei')
const apiKey = ref('')
const apiUrl = ref('')
const showModelSelector = ref(false)
const showSpeechSelector = ref(false)
const showPrivacy = ref(false)

function goBack() {
  router.back()
}

function setTheme(theme) {
  currentTheme.value = theme
  localStorage.setItem('luming-theme', theme)
  applyTheme(theme)
}

function applyTheme(theme) {
  const root = document.documentElement
  if (theme === 'dark') {
    root.style.setProperty('--bg', '#1C1C1E')
    root.style.setProperty('--bg-secondary', '#2C2C2E')
    root.style.setProperty('--text', '#FFFFFF')
    root.style.setProperty('--text-secondary', '#8E8E93')
    root.style.setProperty('--separator', '#38383A')
  } else if (theme === 'warm') {
    root.style.setProperty('--bg', '#FDF6E3')
    root.style.setProperty('--bg-secondary', '#F5EED6')
    root.style.setProperty('--text', '#333333')
    root.style.setProperty('--text-secondary', '#666666')
    root.style.setProperty('--separator', '#E8DCC8')
  } else {
    root.style.setProperty('--bg', '#FFFFFF')
    root.style.setProperty('--bg-secondary', '#F5F5F5')
    root.style.setProperty('--text', '#000000')
    root.style.setProperty('--text-secondary', '#8E8E93')
    root.style.setProperty('--separator', '#E5E5EA')
  }
}

function selectModel(model) {
  currentModel.value = model
  const config = aiModels.find(m => m.value === model)
  currentModelConfig.value = config
  localStorage.setItem('luming-model', model)
  localStorage.setItem('luming-model-config', JSON.stringify(config))
}

function saveApiKey() {
  localStorage.setItem('luming-api-key', apiKey.value)
  localStorage.setItem('luming-api-url', currentModelConfig.value.url)
  alert('API 设置已保存')
}

function exportData() {
  const data = localStorage.getItem('luming-data') || '{}'
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `luming-backup-${new Date().toISOString().split('T')[0]}.json`
  a.click()
  URL.revokeObjectURL(url)
}

function triggerImport() {
  fileInput.value?.click()
}

async function importData(event) {
  const file = event.target.files?.[0]
  if (!file) return
  
  const text = await file.text()
  try {
    const data = JSON.parse(text)
    localStorage.setItem('luming-data', JSON.stringify(data))
    alert('数据导入成功，请刷新页面')
    location.reload()
  } catch (e) {
    alert('导入失败：文件格式不正确')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('luming-theme')
  if (savedTheme) {
    currentTheme.value = savedTheme
    applyTheme(savedTheme)
  }
  
  const savedModel = localStorage.getItem('luming-model')
  if (savedModel) {
    currentModel.value = savedModel
    const config = aiModels.find(m => m.value === savedModel)
    if (config) {
      currentModelConfig.value = config
    }
  }
  
  const savedApiKey = localStorage.getItem('luming-api-key')
  if (savedApiKey) {
    apiKey.value = savedApiKey
  }
  
  const savedApiUrl = localStorage.getItem('luming-api-url')
  if (savedApiUrl) {
    apiUrl.value = savedApiUrl
  }
})
</script>

<style scoped>
.settings-page {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bg-secondary);
  max-width: 430px;
  margin: 0 auto;
  overflow-y: auto;
  z-index: 1600;
}

.settings-page .page-header {
  position: relative;
  padding-top: 14px;
  padding-bottom: 14px;
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

.settings-page .page-title {
  text-align: center;
  padding: 0 60px;
}

.theme-options {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: var(--bg);
  margin-bottom: 20px;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.theme-preview {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  border: 2px solid transparent;
}

.theme-preview.light {
  background: #FFFFFF;
  border-color: var(--separator);
}

.theme-preview.dark {
  background: #1C1C1E;
}

.theme-preview.system {
  background: linear-gradient(135deg, #FFFFFF 50%, #1C1C1E 50%);
}

.theme-preview.warm {
  background: #FDF6E3;
}

.theme-option.active .theme-preview {
  border-color: var(--accent);
}

.theme-name {
  font-size: 13px;
  color: var(--text-secondary);
}

.theme-option.active .theme-name {
  color: var(--accent);
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

.menu-value {
  font-size: 17px;
  color: var(--text-secondary);
}

.menu-arrow {
  color: var(--text-tertiary);
  font-size: 14px;
  margin-left: 4px;
}

.api-key-section {
  margin: 16px;
}

.api-key-input {
  display: flex;
  gap: 8px;
  background: var(--bg);
  padding: 12px;
  border-radius: 12px;
}

.api-key-input .search-input {
  flex: 1;
}

.api-url-input {
  margin-top: 12px;
  display: flex;
  gap: 8px;
  background: var(--bg);
  padding: 12px;
  border-radius: 12px;
}

.api-url-input .search-input {
  flex: 1;
}

.section-label-model {
  font-size: 13px;
  color: var(--text-tertiary);
  margin-top: 12px;
  padding: 0 16px;
}

.model-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px;
}

.model-option {
  padding: 10px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--separator);
  border-radius: 8px;
  font-size: 14px;
  color: var(--text);
  cursor: pointer;
}

.model-option.active {
  background: var(--accent-light);
  border-color: var(--accent);
  color: var(--accent);
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
  max-height: 70vh;
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
</style>
