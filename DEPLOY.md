# 鹿鸣部署指南

## 部署方案：Vercel（前端）+ Railway（后端）

### 第一步：部署后端到 Railway

1. 访问 [Railway.app](https://railway.app)，用 GitHub 登录
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择你的仓库，选择 `backend` 目录
4. 添加环境变量：
   - `GLM_API_KEY`: 你的 API Key
5. Railway 会自动检测 Python 并部署
6. 部署完成后获得后端 URL，如：`https://luming-backend.up.railway.app`

### 第二步：部署前端到 Vercel

1. 访问 [Vercel.com](https://vercel.com)，用 GitHub 登录
2. 点击 "New Project" → Import 你的仓库
3. 设置：
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. 添加环境变量：
   - `VITE_API_URL`: 你的 Railway 后端 URL
5. 点击 Deploy

### 第三步：配置跨域

在后端 Railway 环境变量中添加：
```
ALLOWED_ORIGINS=https://你的vercel域名.vercel.app
```

---

## 本地测试部署

### 构建前端
```bash
cd frontend
npm run build
npm run preview
```

### 构建后端
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 免费额度说明

### Vercel（前端）
- 100GB 带宽/月
- 无限部署
- 自动 HTTPS

### Railway（后端）
- $5 免费额度/月
- 512MB 内存
- 1GB 存储

---

## 常见问题

### Q: 如何更新部署？
A: 推送代码到 GitHub，Vercel 和 Railway 会自动重新部署

### Q: 如何查看日志？
A: 
- Vercel: 项目页面 → Deployments → 点击部署 → Logs
- Railway: 项目页面 → Deployments → 点击部署 → Logs

### Q: 如何绑定自定义域名？
A: 
- Vercel: Settings → Domains → Add
- Railway: Settings → Domains → Add
