# AI Friends 🤖💬

> **一个支持自定义人设、长期记忆、工具调用与 RAG 知识库的 AI 虚拟角色语音陪伴平台。**

AI Friends 是一个基于大语言模型的前后端分离 Web 应用。用户可以创建具备独特人设与背景故事的 AI 虚拟好友,并与他们进行实时流式的文字与语音对话:说话自动断句识别为文字,AI 回复在流式输出文字的同时以所选音色实时合成语音播放。AI 会随着聊天自动积累对用户的长期记忆,能够调用工具(如查询时间、检索知识库),并在回复中融入检索到的领域知识。

> 本项目为个人学习项目,全部代码手写完成,用于系统学习 LLM 应用开发(LangChain / LangGraph / Agent / RAG / 流式传输)与全栈工程实践。

**<img src="frontend/public/favicon.svg" height="16" align="top" alt="AI Friends logo"> 在线体验**:[https://app7917.acapp.acwing.com.cn/](https://app7917.acapp.acwing.com.cn/)

---

## ✨ 功能特性

- **🔐 完整的账号体系**:基于 JWT (simplejwt) 的注册、登录、登出与无感刷新 Token(access token 存于前端、refresh token 存 HttpOnly Cookie,支持 Token 轮换);个人中心支持修改用户名、简介与头像上传(前端集成 Croppie 裁剪)。
- **🎭 个性化 AI 角色创建**:自定义角色名称、头像、背景图与系统人设 (Profile),支持创建、编辑、删除自己的角色。
- **🌐 角色广场**:分页浏览全站公开的 AI 角色,支持按名称 / 简介关键词搜索,一键添加为好友。
- **👥 好友系统**:添加 / 移除 AI 好友,管理我的好友列表(按 `update_time` 倒序;该时间目前在长期记忆更新时刷新,并非每轮互动实时置顶)。
- **💬 流式对话 (Streaming)**:基于 LangGraph 构建对话流,AI 回复通过 SSE (Server-Sent Events) 流式传输,前端逐字渲染;每轮对话入库,并统计输入 / 输出 / 总 Token 消耗。
- **🕘 对话历史持久化**:消息落库存储,支持基于游标 (`last_message_id`) 的历史记录分页加载。注意:入库时用户消息与 AI 回复各截断至 500 字符(`input` 截断至 10000 字符),超长内容的历史记录会丢失截断部分。
- **🛠️ 工具调用 (Function Calling)**:采用 LangGraph 的 ReAct 循环(`agent ⇄ tools`),角色可自主决定是否调用工具。内置「查询当前时间」与「检索知识库」两个工具。
- **🧠 长期记忆**:每累积 10 条对话,将「原有记忆 + 最近 10 轮对话」交给 LLM 提炼,更新并持久化 AI 对用户的「认知」(存于 `Friend.memory`),下轮对话自动注入系统提示。注意:该提炼在本轮 SSE 响应末尾**同步执行**(流式内容已发送完毕,但会延长该请求的收尾时间),尚未接入异步任务队列。
- **📚 知识库增强 (RAG)**:接入 LanceDB 向量数据库,通过自定义 Embedding(阿里云 `text-embedding-v4`)将文档切片入库,对话时按语义相似度检索 Top-3 片段注入上下文。
- **🗣️ 语音交互 (ASR + TTS)**:
  - **语音输入**:前端集成 `@ricky0123/vad-web` 做浏览器端语音活动检测 (VAD),自动断句录音;音频 (PCM) 上传至后端,经 DashScope WebSocket 双工接口调用 `gummy-realtime-v1` 实时识别为文字。
  - **语音输出**:对话时 LLM 流式产生的文本块被同步推送给 TTS WebSocket 任务,合成的音频分片 (mp3, base64) 与文字通过同一条 SSE 流返回前端边播边显。
  - **音色系统**:新增 `Voice` 模型维护音色库(Django Admin 配置公共音色),创建 / 更新角色时从音色库列表中自由选择,角色与音色绑定,对话语音按角色音色合成(TTS 模型 `cosyvoice-v3-flash`)。
  - **音色复刻**:创建 / 更新角色页支持上传音频或浏览器在线录音(MediaRecorder 录制,前端重编码为 16-bit 单声道 WAV),经 DashScope `voice-enrollment` 接口复刻为用户专属音色;自定义音色仅本人可见、可删除(被角色占用时禁止删除),每人上限 10 个,单个音频上限 10MB(wav / mp3 / m4a / aac)。

---

## 🛠️ 技术栈

### 前端 (Frontend)

- **核心框架**:[Vue 3](https://vuejs.org/) (Composition API `<script setup>`) + [Vite](https://vitejs.dev/)
- **状态管理 & 路由**:[Pinia](https://pinia.vuejs.org/) + [Vue Router](https://router.vuejs.org/)(带登录守卫)
- **UI & 样式**:[Tailwind CSS v4](https://tailwindcss.com/)(CSS-first 配置)+ [DaisyUI](https://daisyui.com/)
- **网络与通信**:`axios`(REST,含 401 自动刷新 Token 拦截器)+ `@microsoft/fetch-event-source`(SSE 流式响应)
- **语音**:`@ricky0123/vad-web`(浏览器端语音活动检测,自动断句录音)
- **工程化**:`unplugin-auto-import` + `unplugin-vue-components`(API / 组件自动导入);构建产物直接输出到后端静态目录;`src/js/config/config.js` 通过 `platform` 常量(`vue` / `django` / `cloud`)切换本地开发、本地打包与云端部署三套 API 地址

### 后端 (Backend)

- **核心框架**:[Django](https://www.djangoproject.com/) + Django REST Framework (DRF)
- **AI & Agent**:[LangChain](https://python.langchain.com/) + [LangGraph](https://langchain-ai.github.io/langgraph/),通过 OpenAI 兼容接口调用大模型
- **语音 (ASR / TTS)**:`websockets` 对接 DashScope WebSocket 双工接口——语音识别用 `gummy-realtime-v1`,语音合成用 CosyVoice 系音色(LLM 文本流边生成边送入 TTS 任务,音频与文字合流经 SSE 下发)
- **向量检索 (RAG)**:[LanceDB](https://lancedb.com/) + 自定义 Embedding(`text-embedding-v4`)
- **大模型**:对话默认使用 `deepseek-v4-pro`,可替换为任意兼容 OpenAI 格式的服务(默认对接阿里云百炼 / DashScope)
- **数据库**:SQLite(开发环境)
- **认证**:`djangorestframework-simplejwt`

---

## 🧩 对话链路(核心流程)

```
用户发送消息
      │
      ▼
MessageChatView (SSE)
      │  组装输入:System(全局回复提示 + 角色人设 + 长期记忆)
      │           + 最近 10 轮历史对话
      │           + 当前用户消息
      ▼
LangGraph ReAct Agent ──► [agent 节点] ChatOpenAI(deepseek-v4-pro, streaming)
      │                          │  是否需要工具?
      │            ┌─────────────┴─────────────┐
      │           否                            是
      │            │                            ▼
      │            │                     [tools 节点]
      │            │              get_time / search_knowledge_base(LanceDB)
      │            │                            │
      │            ▼                            └──► 回到 agent
      │      逐 Token 通过 SSE 流式返回前端
      │      (文本块同时推入 TTS WebSocket,合成音频以
      │       base64 mp3 分片与文字一起经同一 SSE 下发)
      ▼
流结束 → 消息入库(含 Token 统计,消息/回复截断至 500 字符)
      → 若累计消息数为 10 的倍数,同步触发长期记忆更新
```

> 语音输入走独立接口:前端 VAD 检测到说话结束后,将 PCM 音频 POST 到 `/api/friend/message/asr/asr/`,后端经 DashScope `gummy-realtime-v1` 识别为文字后直接作为用户消息发送,自动进入上述对话链路。

---

## 📁 核心数据模型

| 模型 | 说明 | 关键字段 |
|------|------|------|
| `UserProfile` | 用户资料,与 Django `User` 一对一关联 | `photo`(头像)、`profile`(简介) |
| `Voice` | TTS 音色库(公共音色 Admin 后台维护,自定义音色由用户复刻生成) | `name`(展示名)、`voice_id`(云端音色 ID,须与 TTS 模型匹配)、`owner`(为空表示公共音色,否则为音色主人 FK)、`audio`(复刻源音频) |
| `Character` | AI 角色 | `author`(创作者 FK)、`name`、`profile`(人设)、`voice`(音色 FK)、`photo`、`background_image` |
| `Friend` | 用户与角色的好友关系,承载专属长期记忆 | `me`(用户 FK)、`character`(角色 FK)、`memory`(长期记忆) |
| `Message` | 每轮对话记录 | `friend`(FK)、`user_message`、`input`、`output`、`input_tokens` / `output_tokens` / `total_tokens` |
| `SystemPrompt` | 全局提示词片段(按 `order_number` 排序拼接) | `title`(如「回复」「记忆」)、`order_number`、`prompt` |

> `SystemPrompt` 是全局配置表,存放「回复」与「记忆」两类提示词模板,可在 Django Admin 后台维护,无需改代码即可调整 AI 的回复风格与记忆总结规则。

---

## 🚀 快速开始

### 环境要求

- Node.js 20.19+ 或 22.12+
- Python 3.12+(作者开发与部署环境为 3.14)
- 一个兼容 OpenAI 接口格式的大模型 API Key(推荐阿里云百炼,新用户有免费额度;需同时支持对话模型与 `text-embedding-v4` 向量模型;使用语音功能还需该 Key 可访问 DashScope 的语音识别 `gummy-realtime-v1` 与 CosyVoice 语音合成)

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
#   WSS_URL=wss://dashscope.aliyuncs.com/api-ws/v1/inference
#   (WSS_URL 为语音识别/合成使用的 DashScope WebSocket 地址。注意:当前对话链路的
#    文字流也经由 TTS WebSocket 任务转发,未配置 WSS_URL 时对话不会返回任何内容,必填)

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
3. **提示词模板**:AI 的回复风格与记忆总结逻辑由 `SystemPrompt` 表驱动。请在 Django Admin 后台创建 `title='回复'` 与 `title='记忆'` 的提示词记录(可分多条,按 `order_number` 拼接),否则 AI 将缺少系统人设约束。
4. **音色库**:在 Django Admin 后台的 `Voice` 表中至少创建一条音色记录(`name` 为展示名,`voice_id` 为云端音色 ID,如 CosyVoice 的 `longanyang`),否则创建角色页的音色下拉为空、无法完成创建。注意 `voice_id` 必须属于 `chat.py` 中 TTS 任务所指定模型的音色列表,否则语音合成会报 `InvalidParameter`。
5. **音色复刻**:「复刻我的音色」功能要求 DashScope 服务器能通过 `MEDIA_URL` 下载到上传的音频,因此**只能在公网可访问的部署环境下生效**——本地开发时 `MEDIA_URL` 指向 `127.0.0.1`,复刻请求会失败(可用内网穿透临时验证)。同时反向代理需放行足够大的请求体(如 nginx 配置 `client_max_body_size 20m;`),否则上传会报 413。
6. **后台管理**:`python manage.py createsuperuser` 创建管理员后可登录 `localhost:8000/admin` 维护数据。注意:此命令创建的用户没有 UserProfile,请勿直接用它登录前端(或在 Django shell 中手动补建 UserProfile)。

### 4. (可选)构建 RAG 知识库

若要启用「检索知识库」工具:

1. 将知识文本放入 `backend/web/documents/data.txt`(UTF-8 编码)。
2. 在 `backend/` 目录下进入 Django shell 执行入库脚本:

   ```powershell
   python manage.py shell
   ```
   ```python
   from web.documents.utils.insert_documents import insert_documents
   insert_documents()   # 按 500 字切片、50 字重叠,写入 LanceDB(表名 my_knowledge_base)
   ```

   脚本会将文档切片、调用 `text-embedding-v4` 生成向量,并写入 `backend/web/documents/lancedb_storage`(每次运行为 `overwrite` 全量重建)。之后对话中问及知识库相关内容,Agent 会自动调用 `search_knowledge_base` 检索 Top-3 片段。

> 注意:入库与检索均使用相对路径 `./web/documents/...`,请确保在 `backend/` 目录下启动进程。另外,`search_knowledge_base` 工具的描述(`graph.py` 中的 docstring)当前写死为「查询阿里云百炼平台相关的信息时调用」,Agent 依据该描述决定是否检索——若放入其他领域的知识文本,请同步修改该 docstring,否则 Agent 可能不会主动调用知识库检索。

---

## ❓ 常见问题

| 问题 | 原因与解决 |
|------|------|
| `venv\Scripts\activate` 报"无法加载模块" | PowerShell 需使用 `.\venv\Scripts\Activate.ps1`,且需先创建虚拟环境 |
| pip 安装报 `UnicodeDecodeError` | requirements.txt 编码问题,用 VS Code 将其另存为 UTF-8 |
| 登录提示"系统异常" | 检查后端是否在运行;若使用 createsuperuser 创建的账号,需先补建 UserProfile |
| 头像显示裂图 | 缺少 `media/user/photos/default.png`,手动放置一张即可 |
| AI 回复不遵循人设 / 记忆不更新 | 检查 `SystemPrompt` 表是否已配置 `title='回复'` 与 `title='记忆'` 的提示词 |
| 知识库检索无结果 | 需先执行 `insert_documents()` 入库,且必须在 `backend/` 目录下启动后端 |
| 创建角色页音色下拉为空 | 数据库无 `Voice` 记录,到 Django Admin 后台添加音色 |
| 文字回复正常但没有语音 / 报 `1007 InvalidParameter` | `voice_id` 与 TTS 模型不匹配(音色须属于 `chat.py` 指定的 `cosyvoice-v3-flash` 的音色列表) |
| 对话无任何回复(整条为空) | `.env` 缺少 `WSS_URL`(文字流也经由 TTS WebSocket 任务转发),或 API Key 无 DashScope 语音服务权限 |
| 麦克风不可用(部署后) | 浏览器 `getUserMedia` 仅在 HTTPS 或 localhost 下可用,生产环境必须配置 HTTPS |
| 音色复刻提示"网络异常" / 接口报 413 | 反向代理请求体上限过小,nginx 配置 `client_max_body_size 20m;` 后重载 |
| 音色复刻提示"复刻失败" | DashScope 无法下载音频:本地开发环境 `MEDIA_URL` 为 `127.0.0.1` 时必然失败,需部署到公网环境;或检查 `.env` 中 `VOICE_URL` 与 API Key 权限 |
| manage.py 命令长时间无输出 | 项目依赖较重,首次加载需 10~30 秒,耐心等待 |

---

## 📖 API 概览

所有接口挂载在根路径下(无额外前缀)。前端对接的 API 基地址由 `src/js/config/config.js` 中的 `platform` 常量决定(当前默认为 `cloud`,指向线上部署地址);本地开发请将其改为 `vue`,即对接 `http://127.0.0.1:8000`。

| 模块 | 核心端点 | 说明 |
|------|------|------|
| **账号** | `POST /api/user/account/login/` `logout/` `register/` `refresh_token/`<br>`GET /api/user/account/get_user_info` | 注册、登录、登出、刷新 Token、获取用户信息 |
| **资料** | `POST /api/user/profile/update/` | 修改个人资料与头像 |
| **角色** | `POST /api/create/character/create/` `update/` `remove/`<br>`GET /api/create/character/get_single/` `get_list/` | 创建、更新、删除、查询自己的 AI 角色 |
| **音色** | `GET /api/create/character/voice/get_list/`<br>`POST /api/create/character/voice/create_custom/` `remove_custom/` | 获取可选音色列表(公共 + 本人自定义);上传 / 录制音频复刻自定义音色、删除自定义音色 |
| **广场** | `GET /api/homepage/index/` | 分页浏览 / 搜索全站公开 AI 角色 |
| **社交** | `POST /api/friend/get_or_create/` `remove/`<br>`GET /api/friend/get_list/` | 添加 / 移除 AI 好友、获取好友列表 |
| **对话** | `POST /api/friend/message/chat/` | 发起 SSE 流式对话,返回文本块与 TTS 音频分片 (base64 mp3) |
| **语音识别** | `POST /api/friend/message/asr/asr/` | 上传 PCM 音频,返回识别文字 |
| **历史** | `GET /api/friend/message/get_history/` | 游标分页拉取历史消息 |

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 授权。
