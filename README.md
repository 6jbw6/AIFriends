# AI Friends 🤖💬

> **一个支持自定义人设、长期记忆、语音交互的 AI 虚拟角色陪伴平台。(开发中)**

AI Friends 是一个基于大语言模型的前后端分离 Web 应用。用户可以创建具备独特人设与背景故事的 AI 虚拟好友,并与他们进行实时流式对话。项目正在持续开发中,目标是构建包含长期记忆、RAG 知识库增强与实时语音交互的完整陪伴体验。

> 本项目为个人学习项目,全部代码手写完成,用于系统学习 LLM 应用开发(LangChain / LangGraph / RAG / 流式传输)与全栈工程实践。

---

## ✨ 功能进度

### 已完成

- **🔐 完整的账号体系**:基于 JWT (simplejwt) 的注册、登录、登出与无感刷新 Token(refresh token 存 HttpOnly Cookie);个人中心支持修改用户名、简介与头像上传。
- **🎭 个性化 AI 角色创建**:自定义角色名称、头像、背景图与系统设定 (Profile),支持创建、编辑、删除自己的角色。
- **🌐 角色广场**:分页浏览全站公开的 AI 角色,一键添加为好友。
- **👥 好友系统**:添加 / 移除 AI 好友,管理我的好友列表。
- **💬 流式对话**:基于 LangGraph 构建对话流,AI 回复通过 SSE (Server-Sent Events) 流式传输,前端逐字渲染。

### 开发中 (Roadmap)

- [ ] **对话历史持久化**:消息入库与历史记录查询,Token 消耗统计
- [ ] **Function Call**:让角色具备调用外部工具的能力
- [ ] **🧠 长期记忆**:后台自动总结对话关键信息,持续更新 AI 对用户的"认知"
- [ ] **📚 知识库增强 (RAG)**:接入 LanceDB 向量数据库,为角色注入领域知识
- [ ] **🗣️ 语音交互**:实时语音识别 (ASR) 输入 + 流式语音合成 (TTS) 播放,自由选择音色

---

## 🛠️ 技术栈

### 前端 (Frontend)

- **核心框架**:[Vue 3](https://vuejs.org/) (Composition API) + [Vite](https://vitejs.dev/)
- **状态管理 & 路由**:[Pinia](https://pinia.vuejs.org/) + Vue Router
- **UI & 样式**:[Tailwind CSS](https://tailwindcss.com/) + [DaisyUI](https://daisyui.com/)
- **网络与通信**:`axios` + `@microsoft/fetch-event-source` (SSE 流式响应)

### 后端 (Backend)

- **核心框架**:[Django](https://www.djangoproject.com/) + Django REST Framework (DRF)
- **AI & Agent**:[LangChain](https://python.langchain.com/) + [LangGraph](https://langchain-ai.github.io/langgraph/),通过 OpenAI 兼容接口调用大模型(默认对接阿里云百炼 / 通义千问,可替换为任意兼容 OpenAI 格式的服务)
- **数据库**:SQLite(开发环境)
- **认证**:`djangorestframework-simplejwt`

---

## 📁 核心数据模型

- `UserProfile`:用户资料,与 Django User 一对一关联(头像、简介)。
- `Character`:AI 角色(创作者、名称、头像、系统设定、背景图)。
- `Friend`:用户与角色的好友关系,后续将在此存储专属长期记忆。

---

## 🚀 快速开始

### 环境要求

- Node.js 20.19+ 或 22.12+
- Python 3.12+
- 一个兼容 OpenAI 接口格式的大模型 API Key(推荐阿里云百炼,新用户有免费额度)

### 1. 后端配置与启动

```powershell
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows PowerShell(注意开头的 .\ 不能省略):
.\venv\Scripts\Activate.ps1
# 若提示"禁止运行脚本",先执行:
#   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# macOS / Linux:
#   source venv/bin/activate

# 4. 安装依赖(国内使用清华镜像加速)
pip install -r ..\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 配置环境变量:在 backend/ 目录下创建 .env 文件,填入:
#   API_KEY=你的API Key
#   API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1

# 6. 数据库迁移
python manage.py migrate

# 7. 启动后端服务(首次启动需加载依赖库,等待十几秒属正常现象)
python manage.py runserver
```

### 2. 前端配置与启动

```powershell
cd frontend

# 安装依赖(国内使用 npmmirror 镜像加速)
npm install --registry=https://registry.npmmirror.com

npm run dev
```

前端运行在 `http://localhost:5173`,后端已配置对应端口的 CORS 许可,直接浏览器访问即可。开发阶段无需 `npm run build`,后端 `localhost:8000` 只提供 API、无页面属正常现象。

### 3. 初始化数据(首次运行必读)

Git 仓库只包含代码,不包含数据库、媒体文件和密钥,首次运行需要:

1. **注册账号**:直接在前端页面注册即可,注册流程会自动创建用户资料。
2. **默认头像**:在 `backend/media/user/photos/` 下放置一张 `default.png` 作为默认头像,否则头像会显示为裂图。
3. **后台管理(可选)**:`python manage.py createsuperuser` 创建管理员后可登录 `localhost:8000/admin`。注意:此命令创建的用户没有 UserProfile,请勿直接用它登录前端(或在 Django shell 中手动补建 UserProfile)。

---

## ❓ 常见问题

| 问题 | 原因与解决 |
|------|------|
| `venv\Scripts\activate` 报"无法加载模块" | PowerShell 需使用 `.\venv\Scripts\Activate.ps1`,且需先创建虚拟环境 |
| pip 安装报 `UnicodeDecodeError` | requirements.txt 编码问题,用 VS Code 将其另存为 UTF-8 |
| 登录提示"系统异常" | 检查后端是否在运行;若使用 createsuperuser 创建的账号,需先补建 UserProfile |
| 头像显示裂图 | 缺少 `media/user/photos/default.png`,手动放置一张即可 |
| manage.py 命令长时间无输出 | 项目依赖较重,首次加载需 10~30 秒,耐心等待 |

---

## 📖 API 概览

| 模块 | 核心端点 | 说明 |
|------|------|------|
| **账号** | `/api/user/account/...` | 注册、登录、登出、获取及刷新 Token、获取用户信息 |
| **资料** | `/api/user/profile/...` | 修改个人资料与头像 |
| **角色** | `/api/create/character/...` | 创建、查询、更新、删除自己的 AI 角色 |
| **广场** | `/api/homepage/index/` | 分页浏览全站公开 AI 角色 |
| **社交** | `/api/friend/...` | 添加 / 移除 AI 好友、获取好友列表 |
| **对话** | `/api/message/chat/` | 发起 SSE 流式对话 |

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 授权。
