# 鹿鸣 - 个人人脉管理助手

记录每一次相遇的温度。

## 功能特性

- **自然语言记录**：通过对话方式记录见面信息，AI 自动解析
- **人脉管理**：管理联系人信息、偏好标签
- **智能待办**：自动提取待办事项，提醒跟进
- **呦呦助手**：AI 助手帮助你管理人脉
- **本地优先**：数据存储在本地，隐私安全

## 技术栈

- 前端：Vue 3 + Vite + PWA
- 后端：Python FastAPI
- 数据库：SQLite
- AI：GLM-5 API

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.9+

### 安装依赖

```bash
# 后端
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 前端
cd frontend
npm install
```

### 配置 API Key

1. 复制环境变量示例文件：
```bash
cd backend
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的 GLM-5 API Key：
```
GLM_API_KEY=your_api_key_here
```

### 启动服务

```bash
# 方式一：使用启动脚本
./start.sh

# 方式二：分别启动
# 后端
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# 前端
cd frontend
npm run dev
```

### 访问应用

- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 项目结构

```
luming/
├── frontend/           # Vue 3 前端
│   ├── src/
│   │   ├── views/      # 页面组件
│   │   ├── components/ # 公共组件
│   │   ├── stores/     # Pinia 状态管理
│   │   └── router/     # 路由配置
│   └── vite.config.js
├── backend/            # FastAPI 后端
│   ├── routes/         # API 路由
│   ├── services/       # 业务逻辑
│   ├── database.py     # 数据库模型
│   └── main.py         # 应用入口
└── start.sh            # 启动脚本
```

## API 接口

### 人脉管理

- `GET /api/persons` - 获取所有人脉
- `GET /api/persons/{id}` - 获取人脉详情
- `POST /api/persons` - 创建人脉
- `PUT /api/persons/{id}` - 更新人脉

### 记录管理

- `GET /api/records` - 获取记录列表
- `POST /api/records` - 创建记录

### 待办管理

- `GET /api/todos` - 获取待办列表
- `PUT /api/todos/{id}` - 更新待办状态

### AI 对话

- `POST /api/chat` - 发送消息
- `POST /api/chat/upload` - 上传文件（图片/录音）

## 开发说明

### 待完善功能

1. **语音识别**：集成讯飞语音识别 API
2. **图片人脸识别**：识别照片中的人物
3. **智能推荐**：根据偏好推荐见面地点
4. **数据同步**：云端备份与同步
5. **提醒功能**：待办事项提醒

### 贡献指南

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT License
