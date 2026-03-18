# 大学生职业规划与实习对接平台

> 职引未来 - 江苏省大学生计算机设计大赛参赛作品

## 项目简介

本平台是一个面向大学生的职业规划与实习对接网站，提供职业测评、简历编辑、实习岗位浏览与投递、经验分享等功能。

## 技术栈

- **后端**: Python 3.x + Flask
- **前端**: HTML5 + CSS3 + JavaScript + Bootstrap 5
- **数据库**: SQLite
- **图表**: Chart.js

## 项目结构

```
career-platform/
├── app.py                 # Flask 主应用
├── requirements.txt       # Python 依赖
├── db/                    # 数据库目录
│   └── career.db         # SQLite 数据库文件
├── static/               # 静态资源
│   ├── css/
│   │   └── style.css     # 自定义样式
│   └── js/
│       └── main.js       # 公共 JavaScript
└── templates/            # HTML 模板
    ├── index.html        # 首页
    ├── login.html        # 登录页
    ├── register.html     # 注册页
    ├── profile.html      # 个人中心
    ├── resume.html       # 简历编辑
    ├── internships.html  # 实习岗位列表
    ├── internship_detail.html  # 岗位详情
    ├── assessment.html   # 职业测评
    ├── articles.html     # 经验分享列表
    ├── article_detail.html     # 文章详情
    └── admin.html        # 后台管理
```

## 安装与运行

### 1. 安装 Python 依赖

```bash
pip install flask flask-cors
```

或者使用 requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. 运行项目

```bash
python app.py
```

### 3. 访问网站

打开浏览器访问：http://127.0.0.1:5000

## 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 学生 | student1 | 123456 |
| 企业 | hr1 | 123456 |
| 管理员 | admin | 123456 |

## 功能模块

### 前台功能

1. **首页** - 轮播图、快速入口、热门实习、最新文章
2. **用户认证** - 注册、登录、退出
3. **实习岗位** - 列表浏览、筛选、详情查看、在线投递
4. **简历编辑** - 在线创建和编辑个人简历
5. **职业测评** - 霍兰德职业兴趣测试
6. **经验分享** - 浏览面试经验、简历指导等文章
7. **个人中心** - 查看投递记录、简历、测评结果

### 后台管理

1. **数据概览** - 用户统计、岗位统计、数据可视化图表
2. **用户管理** - 查看用户列表
3. **岗位管理** - 查看和管理实习岗位
4. **投递管理** - 查看投递记录

## 主要 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/login | POST | 用户登录 |
| /api/register | POST | 用户注册 |
| /api/logout | POST | 退出登录 |
| /api/internships | GET | 获取实习岗位列表 |
| /api/internships/<id> | GET | 获取岗位详情 |
| /api/apply | POST | 投递简历 |
| /api/my-applications | GET | 获取我的投递 |
| /api/resume | GET/POST | 获取/保存简历 |
| /api/articles | GET | 获取文章列表 |
| /api/articles/<id> | GET | 获取文章详情 |
| /api/assessments/holland | GET | 获取测评题目 |
| /api/assessments/submit | POST | 提交测评结果 |
| /api/stats | GET | 获取统计数据 |

## 数据库表

- `users` - 用户表
- `companies` - 企业表
- `internships` - 实习岗位表
- `resumes` - 简历表
- `applications` - 投递记录表
- `assessments` - 测评结果表
- `articles` - 经验分享表
- `appointments` - 预约记录表

## 团队成员

- 成员 1：前端开发
- 成员 2：后端开发
- 成员 3：内容管理与测试

## 比赛信息

- **比赛名称**: 江苏省大学生计算机设计大赛
- **参赛类别**: 软件应用与开发类
- **开发时间**: 2026 年

## 注意事项

1. 本项目使用 SQLite 数据库，数据存储在 `db/career.db` 文件中
2. 首次运行时会自动创建数据库表并插入示例数据
3. 密码使用 MD5 加密存储（仅用于演示，生产环境请使用更安全的加密方式）
4. 本项目仅供学习和比赛使用

## 许可证

本项目仅供学习和比赛使用。
