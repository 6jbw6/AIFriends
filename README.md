# AI Friends

与 AI 角色实时语音聊天的全栈应用。

## 功能特性

- **AI 角色创建** — 自定义角色的名字、头像、性格设定、背景图、语音音色
- **实时对话** — 基于 SSE 的流式聊天，支持文本 + 语音双模态交互
- **语音合成 (TTS)** — AI 回复自动转为语音（CosyVoice），支持边生成边播放
- **语音识别 (ASR)** — 语音输入转文字，无需打字
- **长期记忆** — 自动总结近期对话并更新角色记忆，让 AI 朋友更懂你
- **角色广场** — 浏览、搜索其他用户创建的 AI 角色
- **JWT 认证** — 安全的用户注册/登录体系

## 技术栈

| 层 | 技术 |
|---|------|
| 前端 | Vue 3 + Vite + Tailwind CSS + DaisyUI + Pinia |
| 后端 | Django 6.0 + Django REST Framework |
| AI 对话 | LangChain + LangGraph + OpenAI |
| 向量检索 | LanceDB |
| 实时通信 | SSE (Server-Sent Events) + WebSocket |
| 语音 | CosyVoice (TTS) + Gummy-Realtime (ASR) |
| 认证 | Simple JWT |

## 项目结构

```
aifriends/
├── backend/                  # Django 后端
│   ├── backend/              # 项目配置 (settings, urls, wsgi, asgi)
│   ├── web/                  # 主应用
│   │   ├── models/           # 数据模型 (User, Character, Friend, Message)
│   │   ├── views/            # 视图逻辑
│   │   │   ├── user/         # 用户认证与资料
│   │   │   ├── create/       # AI 角色 CRUD + 语音管理
│   │   │   ├── friend/       # 好友关系 + 聊天 + ASR + 记忆
│   │   │   └── homepage/     # 角色广场
│   │   ├── documents/        # RAG 知识库 (LanceDB)
│   │   └── migrations/       # 数据库迁移
│   └── manage.py
├── frontend/                 # Vue 3 前端
│   ├── src/
│   │   ├── views/            # 页面组件
│   │   ├── components/       # 通用组件
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # Pinia 状态管理
│   │   └── js/               # 工具函数
│   └── vite.config.js
└── requirements.txt
```

## 快速开始

### 环境要求

- Python 3.12+
- Node.js 20.19+ / 22.12+
- 有效的 OpenAI API Key

### 1. 后端配置

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r ../requirements.txt
```

创建 `.env` 文件并配置环境变量：

```env
API_KEY=your_api_key_here
WSS_URL=wss://your-websocket-service-url
OPENAI_API_KEY=your_openai_key
OPENAI_BASE_URL=https://api.openai.com/v1
```

数据库迁移与启动：

```bash
python manage.py migrate
python manage.py runserver
```

### 2. 前端配置

```bash
cd frontend
npm install
npm run dev
```

前端默认运行在 `http://localhost:5173`，已配置 CORS 允许该来源。

### 3. 使用 RAG 知识库（可选）

在 `backend/web/documents/data.txt` 中放入知识库文本，然后运行：

```bash
python -m web.documents.utils.insert_documents
```

## API 概览

| 端点 | 说明 |
|------|------|
| `POST /api/user/account/register/` | 用户注册 |
| `POST /api/user/account/login/` | 用户登录 |
| `POST /api/user/account/refresh_token/` | 刷新 JWT Token |
| `GET /api/user/account/get_user_info/` | 获取用户信息 |
| `POST /api/user/profile/update/` | 更新个人资料 |
| `POST /api/create/character/create/` | 创建 AI 角色 |
| `POST /api/create/character/update/` | 更新 AI 角色 |
| `POST /api/create/character/remove/` | 删除 AI 角色 |
| `GET /api/create/character/get_list/` | 获取我的角色列表 |
| `GET /api/create/character/get_single/` | 获取单个角色详情 |
| `GET /api/create/character/voice/get_list/` | 获取可用语音列表 |
| `GET /api/homepage/index/` | 角色广场（分页 + 搜索） |
| `POST /api/friend/get_or_create/` | 添加 AI 好友 |
| `POST /api/friend/remove/` | 删除好友 |
| `GET /api/friend/get_list/` | 好友列表 |
| `POST /api/friend/message/chat/` | 发送消息（SSE 流式响应） |
| `GET /api/friend/message/get_history/` | 获取聊天历史 |
| `POST /api/friend/message/asr/asr/` | 语音转文字 |

## 许可证

MIT
