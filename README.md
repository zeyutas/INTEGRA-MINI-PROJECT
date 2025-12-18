# Integra Mini Project Monorepo

一个基于 Django REST Framework 后端和 Vue 2 前端的单体仓库项目，使用 npm workspaces 和 Turborepo 进行管理。

## 📁 项目结构

```
integra-mini-project/
├── apps/
│   ├── user-profile-backend/     # Django REST API 后端
│   │   ├── integra_core/         # Django 核心配置
│   │   ├── users/                # 用户模块
│   │   ├── manage.py             # Django 管理脚本
│   │   ├── requirements.txt      # Python 依赖
│   │   └── db.sqlite3           # SQLite 数据库
│   └── user-profile-frontend/    # Vue 2 + Element UI 前端
│       ├── src/                  # 源代码
│       ├── public/               # 静态资源
│       └── package.json          # 前端依赖配置
├── packages/
│   └── shared-types/             # TypeScript 共享类型定义
├── package.json                  # 根项目配置
└── turbo.json                    # Turborepo 配置
```

## 🔧 前置要求

### 必需软件
- **Python 3.11+**（推荐 3.11 或更高版本）
- **Node.js 16+** 和 **npm 10+**
- **Git**

### 推荐工具
- **Visual Studio Code** 或其他代码编辑器
- **Postman** 或类似 API 测试工具

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd integra-mini-project
```

### 2. 安装依赖

#### 安装前端依赖（在项目根目录）
```bash
npm install
```
这会安装 Turborepo 和所有工作区依赖（前端 + shared-types）。

#### 安装后端依赖
```bash
cd apps/user-profile-backend

# 创建 Python 虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install -r requirements-dev.txt
```

## ⚙️ 后端配置与运行

### 1. 环境变量配置

在 `apps/user-profile-backend/` 目录下创建 `.env` 文件：

```bash
cd apps/user-profile-backend
```

创建 `.env` 文件，添加以下配置：

```env
# Django 配置
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库配置（使用 SQLite）
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# CORS 配置
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080

# JWT 配置
JWT_ACCESS_TOKEN_LIFETIME=60  # 分钟
JWT_REFRESH_TOKEN_LIFETIME=1440  # 分钟（24小时）
```

### 2. 数据库初始化

```bash
# 确保在 user-profile-backend 目录并激活虚拟环境
cd apps/user-profile-backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 执行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser
```

### 3. 运行后端服务

```bash
# 启动开发服务器（默认端口 8000）
python manage.py runserver

# 或指定端口
python manage.py runserver 8000
```

后端服务将运行在 `http://localhost:8000`

#### 后端 API 端点
- **API 文档**: `http://localhost:8000/api/schema/swagger-ui/`
- **用户注册**: `POST http://localhost:8000/api/users/register/`
- **用户登录**: `POST http://localhost:8000/api/users/login/`
- **获取用户信息**: `GET http://localhost:8000/api/users/profile/`
- **更新用户信息**: `PUT http://localhost:8000/api/users/profile/`

### 4. 后端常用命令

```bash
# 运行测试
python manage.py test

# 运行特定测试
python manage.py test users.tests.test_views_profile

# 创建新的应用
python manage.py startapp <app_name>

# 收集静态文件（生产环境）
python manage.py collectstatic

# 查看所有 URL 路由
python manage.py show_urls  # 需要安装 django-extensions
```

## 🎨 前端配置与运行

### 1. 环境变量配置

在 `apps/user-profile-frontend/` 目录下创建 `.env` 文件：

```env
# API 基础地址
VUE_APP_API_BASE_URL=http://localhost:8000

# 开发环境代理目标
VUE_APP_API_PROXY_TARGET=http://localhost:8000
```

可选：创建 `.env.production` 用于生产环境：

```env
VUE_APP_API_BASE_URL=https://your-production-api.com
```

### 2. 运行前端服务

#### 方式一：从根目录运行（推荐）
```bash
# 在项目根目录
npm run dev
```

#### 方式二：仅运行前端
```bash
npm run dev -- --filter user-profile-frontend
```

#### 方式三：直接在前端目录运行
```bash
cd apps/user-profile-frontend
npm run serve
```

前端服务将运行在 `http://localhost:8080`

### 3. 前端常用命令

```bash
# 代码检查
npm run lint

# 构建生产版本
cd apps/user-profile-frontend
npm run build

# 构建后的文件在 dist/ 目录
```

## 🔄 完整开发流程

### 启动开发环境

**需要开启两个终端窗口：**

#### 终端 1 - 启动后端
```bash
cd apps/user-profile-backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
python manage.py runserver
```

#### 终端 2 - 启动前端
```bash
# 在项目根目录
npm run dev
```

然后访问：
- 前端应用：`http://localhost:8080`
- 后端 API：`http://localhost:8000`
- API 文档：`http://localhost:8000/api/schema/swagger-ui/`

## 📦 依赖管理

### 后端依赖
主要依赖（`requirements.txt`）：
- `Django==5.2.9` - Web 框架
- `djangorestframework==3.16.1` - REST API 框架
- `djangorestframework-simplejwt==5.5.1` - JWT 认证
- `django-cors-headers==4.9.0` - CORS 支持
- `drf-spectacular` - API 文档生成

添加新的 Python 依赖：
```bash
pip install <package-name>
pip freeze > requirements.txt
```

### 前端依赖
主要依赖：
- `vue@2.7.16` - 前端框架
- `vue-router@3.6.5` - 路由管理
- `element-ui@2.15.14` - UI 组件库
- `axios@1.13.2` - HTTP 客户端

添加新的 npm 依赖：
```bash
cd apps/user-profile-frontend
npm install <package-name>
```

## 🧪 测试

### 后端测试
```bash
cd apps/user-profile-backend
venv\Scripts\activate
python manage.py test
```

### 前端测试
```bash
cd apps/user-profile-frontend
npm run test
```

## 🏗️ 生产部署

### 后端部署准备

1. **更新配置**
```bash
# 设置生产环境变量
DEBUG=False
SECRET_KEY=<生成强密钥>
ALLOWED_HOSTS=your-domain.com
```

2. **收集静态文件**
```bash
python manage.py collectstatic --noinput
```

3. **使用生产级服务器**（如 Gunicorn）
```bash
pip install gunicorn
gunicorn integra_core.wsgi:application --bind 0.0.0.0:8000
```

### 前端部署准备

1. **构建生产版本**
```bash
cd apps/user-profile-frontend
npm run build
```

2. **部署 dist/ 目录**
将 `dist/` 目录内容部署到静态文件服务器（Nginx、Apache 或 CDN）。

## 📝 开发规范

### Git 提交规范
- 保持敏感信息（`.env`、数据库文件、API 密钥）不要提交到 Git
- 提交前运行 lint 和测试
- 使用清晰的提交信息

### 代码规范
- **后端**: 遵循 PEP 8 Python 编码规范
- **前端**: 使用 ESLint 配置（Standard 风格）

### 分支管理
- `main` - 生产环境代码
- `develop` - 开发环境代码
- `feature/*` - 功能分支
- `bugfix/*` - 修复分支

## 🐛 常见问题

### 后端问题

**问题：`ModuleNotFoundError: No module named 'xxx'`**
```bash
# 确保虚拟环境已激活并重新安装依赖
venv\Scripts\activate
pip install -r requirements.txt
```

**问题：数据库迁移错误**
```bash
# 删除迁移文件并重新生成
python manage.py migrate --fake-initial
```

**问题：CORS 错误**
检查 `CORS_ALLOWED_ORIGINS` 配置是否包含前端地址。

### 前端问题

**问题：API 请求失败**
- 确认后端服务正在运行
- 检查 `VUE_APP_API_BASE_URL` 配置
- 查看浏览器开发者工具的网络请求

**问题：端口被占用**
```bash
# 使用不同端口
npm run serve -- --port 8081
```

## 📚 技术栈

### 后端
- **框架**: Django 5.2 + Django REST Framework 3.16
- **认证**: JWT (Simple JWT)
- **数据库**: SQLite（开发）/ PostgreSQL（生产推荐）
- **API 文档**: drf-spectacular (OpenAPI 3.0)

### 前端
- **框架**: Vue 2.7
- **路由**: Vue Router 3.6
- **UI 库**: Element UI 2.15
- **HTTP 客户端**: Axios 1.13
- **构建工具**: Vue CLI 4.5

### 开发工具
- **包管理**: Turborepo 2.2 + npm workspaces
- **代码规范**: ESLint + Babel

## 📄 许可证

本项目仅供学习和开发使用。

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📧 联系方式

如有问题或建议，请联系项目维护者。
