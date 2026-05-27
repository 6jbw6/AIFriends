# AI Friends 🤖💬

> **一个支持自定义设定、长期记忆、语音交互的智能虚拟角色陪伴平台。**

AI Friends 是一个基于大语言模型、语音识别与合成技术的全栈 Web 应用。通过本项目，用户可以创建具备独特人设、音色和背景故事的 AI 虚拟好友，并与他们进行实时流式语音和文字交流。项目内置记忆机制，让 AI 能够“记住”你们之间的互动，提供更拟人化的陪伴体验。

---

## ✨ 核心特性

- **🎭 个性化 AI 角色创建**：高度定制化的虚拟角色，支持上传角色头像、背景图，定义角色性格与背景故事，并自由选择专属合成音色。
- **🗣️ 多模态实时通讯**：支持打字聊天和实时语音输入 (ASR)，AI 回复采用 SSE (Server-Sent Events) 流式传输，并可边生成边进行语音合成 (TTS)。
- **🧠 记忆与认知系统**：
  - **短期记忆**：在单次会话中保持上下文连贯。
  - **长期记忆**：AI 会在后台自动总结关键对话信息，不断更新对用户的“认知”，实现真正的长期陪伴。
- **📚 知识库增强 (RAG)**：底层接入 LanceDB 向量数据库，可导入专业领域知识，让角色不仅有性格，还能具备丰富的专业知识。
- **🌐 角色广场**：探索和添加其他用户创建的优秀公开角色为好友。
- **🔐 完整的安全认证体系**：基于 JWT 认证的注册、登录及个人中心管理。

---

## 🛠️ 技术栈

本项目采用前后端分离架构，核心技术选型如下：

### 前端 (Frontend)
- **核心框架**：[Vue 3](https://vuejs.org/) (Composition API) + [Vite](https://vitejs.dev/)
- **状态管理 & 路由**：[Pinia](https://pinia.vuejs.org/) + Vue Router
- **UI & 样式**：[Tailwind CSS](https://tailwindcss.com/) + [DaisyUI](https://daisyui.com/)
- **语音前端**：`@ricky0123/vad-web` (浏览器端静音检测与录音)
- **网络与通信**：`axios` + `@microsoft/fetch-event-source` (流式响应)

### 后端 (Backend)
- **核心框架**：[Django](https://www.djangoproject.com/) + Django REST Framework (DRF)
- **AI & Agent**：[LangChain](https://python.langchain.com/) + [LangGraph](https://langchain-ai.github.io/langgraph/) + OpenAI API (兼容通用大模型 API)
- **数据库**：SQLite (关系型数据) + [LanceDB](https://lancedb.com/) (向量存储)
- **语音服务**：CosyVoice (高拟真语音合成) + Gummy-Realtime (实时语音识别)
- **认证**：`djangorestframework-simplejwt`

---

## 📁 核心数据模型

系统的核心逻辑围绕以下数据模型展开：
- `UserProfile`: 用户个人中心与账号体系。
- `Character`: AI 角色（包含创作者、名称、头像、系统设定/Profile、背景图、专属音色等）。
- `Friend`: 缔结的好友关系，**独立存储该用户与该角色之间的专属长期记忆 (`memory` 字段)**。
- `Message`: 对话历史及 Token 消耗统计。
- `SystemPrompt`: 后台可配置的系统级 Prompt 链。

---

## 🚀 快速开始

### 环境前置要求
- Node.js 20.19+ 或 22.12+
- Python 3.12+
- OpenAI API Key（或支持 OpenAI 接口格式的任意大模型 API）

### 1. 后端配置与启动

```bash
# 1. 进入后端目录
cd backend

# 2. 创建并激活虚拟环境 (可选但推荐)
python -m venv venv
# Windows 激活方式:
source venv/Scripts/activate
# macOS/Linux 激活方式:
# source venv/bin/activate

# 3. 安装依赖包
pip install -r ../requirements.txt

# 4. 环境变量配置
# 在 backend/ 目录下创建 .env 文件，并填入以下内容：
# API_KEY=your_api_key_here
# WSS_URL=wss://your-websocket-service-url
# OPENAI_API_KEY=your_openai_key
# OPENAI_BASE_URL=https://api.openai.com/v1

# 5. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 6. 启动后端服务
python manage.py runserver
```

> **可选操作：构建本地知识库 (RAG)**
> 如果你想为角色注入额外的资料，可将文本内容放入 `backend/web/documents/data.txt`，随后执行：
> `python -m web.documents.utils.insert_documents`


### 2. 前端配置与启动

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装 Node 依赖包
npm install

# 3. 启动开发服务器
npm run dev
```

前端启动后，默认运行在 `http://localhost:5173`。后端 Django 已经配置了对应端口的 CORS 跨域许可，可以直接打开浏览器访问该地址体验。

---

## 📖 API 概览

系统对外提供的 RESTful 接口包含但不限于：

| 模块 | 核心端点 | 说明 |
|------|------|------|
| **账号** | `/api/user/account/...` | 注册、登录、获取及刷新 Token、获取用户信息 |
| **资料** | `/api/user/profile/...` | 修改个人主页和基础信息 |
| **角色** | `/api/create/character/...` | 创建、更新、删除自己的 AI 角色，获取所有可用语音音色列表 |
| **广场** | `/api/homepage/index/` | 分页浏览全站公开 AI 角色，支持关键字搜索 |
| **社交** | `/api/friend/...` | 添加 AI 为好友、移除好友、获取我的好友列表 |
| **对话** | `/api/friend/message/...` | 发起流式对话 (`chat`)、查看历史消息 (`get_history`)、语音转文本 (`asr/asr`) |

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 授权。
