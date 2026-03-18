"""
大学生职业规划与实习对接平台
Flask 主应用入口
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'career_platform_secret_key_2026'
CORS(app)

# 数据库文件路径
DB_PATH = 'db/career.db'

# ==================== 数据库初始化 ====================
def init_db():
    """初始化数据库，创建所有表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role TEXT DEFAULT 'student',
            school TEXT,
            major TEXT,
            grade TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 企业表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            company_name TEXT,
            industry TEXT,
            scale TEXT,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # 实习岗位表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            requirements TEXT,
            salary TEXT,
            location TEXT,
            type TEXT,
            deadline DATE,
            status TEXT DEFAULT 'active',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    ''')

    # 简历表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            objective TEXT,
            education TEXT,
            skills TEXT,
            experience TEXT,
            awards TEXT,
            template_id INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # 投递记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            internship_id INTEGER,
            status TEXT DEFAULT 'pending',
            applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users(id),
            FOREIGN KEY (internship_id) REFERENCES internships(id)
        )
    ''')

    # 职业测评表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            result TEXT,
            score TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # 经验分享表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            content TEXT,
            category TEXT,
            views INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # 预约记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            counselor_id INTEGER,
            appointment_time DATETIME,
            status TEXT DEFAULT 'pending',
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users(id),
            FOREIGN KEY (counselor_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("数据库初始化完成!")

# ==================== 辅助函数 ====================
def hash_password(password):
    """密码加密"""
    return hashlib.md5(password.encode()).hexdigest()

def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_sample_data():
    """插入示例数据"""
    conn = get_db()
    cursor = conn.cursor()

    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # 插入示例用户
    users = [
        ('admin', hash_password('123456'), 'admin@career.com', '13800138000', 'admin', '系统管理员', '', ''),
        ('student1', hash_password('123456'), 'student1@test.com', '13800138001', 'student', '南京大学', '计算机科学', '2023'),
        ('student2', hash_password('123456'), 'student2@test.com', '13800138002', 'student', '东南大学', '软件工程', '2024'),
        ('hr1', hash_password('123456'), 'hr@company1.com', '13800138003', 'enterprise', '', '', ''),
    ]

    cursor.executemany('''
        INSERT INTO users (username, password, email, phone, role, school, major, grade)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', users)

    # 插入示例企业
    cursor.executemany('''
        INSERT INTO companies (user_id, company_name, industry, scale, description)
        VALUES (?, ?, ?, ?, ?)
    ''', [
        (4, '阿里巴巴', '互联网', '10000+', '全球知名的电子商务和科技公司'),
        (4, '腾讯科技', '互联网', '10000+', '中国领先的互联网增值服务提供商'),
        (4, '华为技术', '通信', '10000+', '全球领先的信息与通信技术解决方案提供商'),
        (4, '字节跳动', '互联网', '5000-10000', '全球领先的技术公司，打造多款知名应用'),
    ])

    # 插入示例实习岗位
    internships = [
        (1, '前端开发实习生', '负责公司 Web 产品的前端开发', '熟悉 HTML/CSS/JavaScript，了解 React 或 Vue', '200-300 元/天', '杭州', '实习', '2026-06-30'),
        (1, '后端开发实习生', '参与后端服务开发与维护', '熟悉 Python/Java，了解数据库和 Linux', '250-350 元/天', '北京', '实习', '2026-06-30'),
        (2, '产品运营实习生', '协助产品经理进行用户运营', '沟通能力强，有数据分析基础', '150-250 元/天', '深圳', '实习', '2026-07-31'),
        (2, 'UI 设计实习生', '负责产品界面设计', '熟练使用 Figma/Sketch，有设计作品集', '200-300 元/天', '广州', '实习', '2026-06-30'),
        (3, '测试开发实习生', '参与自动化测试框架开发', '熟悉 Python/Java，了解测试理论', '200-300 元/天', '南京', '实习', '2026-08-31'),
        (3, '数据分析实习生', '负责业务数据分析与可视化', '熟悉 SQL、Python，了解统计学', '250-350 元/天', '上海', '实习', '2026-07-31'),
        (4, '内容运营实习生', '负责短视频内容运营', '对热点敏感，有文案能力', '180-280 元/天', '北京', '实习', '2026-06-30'),
        (4, '算法工程实习生', '参与推荐算法研发', '熟悉机器学习，有 Python/C++ 基础', '300-500 元/天', '北京', '实习', '2026-08-31'),
    ]

    cursor.executemany('''
        INSERT INTO internships (company_id, title, description, requirements, salary, location, type, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', internships)

    # 插入示例文章
    articles = [
        (2, '如何准备互联网大厂面试', '面试准备是求职过程中最重要的环节...', '面试经验'),
        (2, '简历怎么写才能吸引 HR', '一份好的简历应该注意以下几点...', '简历指导'),
        (3, '我的腾讯实习经历分享', '去年有幸获得腾讯的实习 offer，在这里分享一下...', '实习经验'),
        (3, '非科班如何转行程序员', '我原本的专业是英语，通过自学成功转行...', '职业发展'),
    ]

    cursor.executemany('''
        INSERT INTO articles (user_id, title, content, category)
        VALUES (?, ?, ?, ?)
    ''', articles)

    conn.commit()
    conn.close()
    print("示例数据插入完成!")

# ==================== 路由 ====================

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/login')
def login_page():
    """登录页"""
    return render_template('login.html')

@app.route('/register')
def register_page():
    """注册页"""
    return render_template('register.html')

# ==================== API 接口 ====================

@app.route('/api/login', methods=['POST'])
def api_login():
    """用户登录"""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        return jsonify({'success': True, 'message': '登录成功', 'user': {'id': user['id'], 'username': user['username'], 'role': user['role']}})
    else:
        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

@app.route('/api/register', methods=['POST'])
def api_register():
    """用户注册"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role', 'student')
    school = data.get('school', '')
    major = data.get('major', '')
    grade = data.get('grade', '')

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (username, password, email, phone, role, school, major, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, hash_password(password), email, phone, role, school, major, grade))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': '注册成功'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': '用户名已存在'}), 400

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """用户登出"""
    session.clear()
    return jsonify({'success': True, 'message': '已退出登录'})

@app.route('/api/check-login')
def api_check_login():
    """检查登录状态"""
    if 'user_id' in session:
        return jsonify({'logged_in': True, 'user': {'id': session['user_id'], 'username': session['username'], 'role': session['role']}})
    return jsonify({'logged_in': False})

@app.route('/api/internships')
def get_internships():
    """获取实习岗位列表"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.*, c.company_name
        FROM internships i
        JOIN companies c ON i.company_id = c.id
        WHERE i.status = 'active'
        ORDER BY i.created_at DESC
    ''')
    rows = cursor.fetchall()
    conn.close()

    internships = [dict(row) for row in rows]
    return jsonify({'success': True, 'data': internships})

@app.route('/api/internships/<int:id>')
def get_internship(id):
    """获取实习岗位详情"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.*, c.company_name, c.description as company_desc, c.industry, c.scale
        FROM internships i
        JOIN companies c ON i.company_id = c.id
        WHERE i.id = ?
    ''', (id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({'success': True, 'data': dict(row)})
    return jsonify({'success': False, 'message': '岗位不存在'}), 404

@app.route('/api/apply', methods=['POST'])
def apply_internship():
    """投递简历"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'}), 401

    data = request.json
    internship_id = data.get('internship_id')

    conn = get_db()
    cursor = conn.cursor()

    # 检查是否已投递
    cursor.execute('''
        SELECT * FROM applications WHERE student_id = ? AND internship_id = ?
    ''', (session['user_id'], internship_id))

    if cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': '您已投递过该岗位'})

    cursor.execute('''
        INSERT INTO applications (student_id, internship_id)
        VALUES (?, ?)
    ''', (session['user_id'], internship_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': '投递成功'})

@app.route('/api/my-applications')
def get_my_applications():
    """获取我的投递"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'}), 401

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, i.title, i.salary, i.location, c.company_name, a.status, a.applied_at
        FROM applications a
        JOIN internships i ON a.internship_id = i.id
        JOIN companies c ON i.company_id = c.id
        WHERE a.student_id = ?
        ORDER BY a.applied_at DESC
    ''', (session['user_id'],))
    rows = cursor.fetchall()
    conn.close()

    return jsonify({'success': True, 'data': [dict(row) for row in rows]})

@app.route('/api/resume', methods=['GET'])
def get_resume():
    """获取我的简历"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'}), 401

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resumes WHERE user_id = ?', (session['user_id'],))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({'success': True, 'data': dict(row)})
    return jsonify({'success': True, 'data': None})

@app.route('/api/resume', methods=['POST'])
def save_resume():
    """保存简历"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'}), 401

    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    # 检查是否已有简历
    cursor.execute('SELECT id FROM resumes WHERE user_id = ?', (session['user_id'],))
    existing = cursor.fetchone()

    if existing:
        cursor.execute('''
            UPDATE resumes SET name=?, objective=?, education=?, skills=?, experience=?, awards=?, template_id=?, updated_at=CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (data.get('name'), data.get('objective'), data.get('education'),
              data.get('skills'), data.get('experience'), data.get('awards'),
              data.get('template_id', 1), session['user_id']))
    else:
        cursor.execute('''
            INSERT INTO resumes (user_id, name, objective, education, skills, experience, awards, template_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], data.get('name'), data.get('objective'),
              data.get('education'), data.get('skills'), data.get('experience'),
              data.get('awards'), data.get('template_id', 1)))

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': '简历保存成功'})

@app.route('/api/articles')
def get_articles():
    """获取文章列表"""
    category = request.args.get('category')

    conn = get_db()
    cursor = conn.cursor()

    if category:
        cursor.execute('SELECT a.*, u.username FROM articles a JOIN users u ON a.user_id = u.id WHERE a.category = ? ORDER BY a.created_at DESC', (category,))
    else:
        cursor.execute('SELECT a.*, u.username FROM articles a JOIN users u ON a.user_id = u.id ORDER BY a.created_at DESC')

    rows = cursor.fetchall()
    conn.close()

    return jsonify({'success': True, 'data': [dict(row) for row in rows]})

@app.route('/api/articles/<int:id>')
def get_article(id):
    """获取文章详情"""
    conn = get_db()
    cursor = conn.cursor()

    # 增加浏览量
    cursor.execute('UPDATE articles SET views = views + 1 WHERE id = ?', (id,))
    cursor.execute('SELECT a.*, u.username FROM articles a JOIN users u ON a.user_id = u.id WHERE a.id = ?', (id,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()

    if row:
        return jsonify({'success': True, 'data': dict(row)})
    return jsonify({'success': False, 'message': '文章不存在'}), 404

@app.route('/api/assessments/holland')
def get_holland_test():
    """获取霍兰德职业兴趣测试题目"""
    questions = [
        {"id": 1, "question": "我喜欢动手操作机械、工具", "type": "R"},
        {"id": 2, "question": "我喜欢研究科学问题、做实验", "type": "I"},
        {"id": 3, "question": "我喜欢创作音乐、绘画或写作", "type": "A"},
        {"id": 4, "question": "我喜欢帮助他人、关心他人感受", "type": "S"},
        {"id": 5, "question": "我喜欢组织活动、带领团队", "type": "E"},
        {"id": 6, "question": "我喜欢处理数据、整理文档", "type": "C"},
        {"id": 7, "question": "我喜欢修理电器、制作模型", "type": "R"},
        {"id": 8, "question": "我喜欢分析数据、解决逻辑问题", "type": "I"},
        {"id": 9, "question": "我喜欢参加艺术活动、欣赏作品", "type": "A"},
        {"id": 10, "question": "我喜欢与人交流、倾听他们的问题", "type": "S"},
        {"id": 11, "question": "我喜欢竞争、争取领导地位", "type": "E"},
        {"id": 12, "question": "我喜欢按部就班、遵循规则", "type": "C"},
        {"id": 13, "question": "我喜欢户外活动、体力劳动", "type": "R"},
        {"id": 14, "question": "我喜欢探索未知、追求真理", "type": "I"},
        {"id": 15, "question": "我喜欢自由表达、展现个性", "type": "A"},
        {"id": 16, "question": "我喜欢 teaching、培训他人", "type": "S"},
        {"id": 17, "question": "我喜欢销售、说服他人", "type": "E"},
        {"id": 18, "question": "我喜欢记录信息、管理档案", "type": "C"},
    ]
    return jsonify({'success': True, 'data': questions})

@app.route('/api/assessments/submit', methods=['POST'])
def submit_assessment():
    """提交测评结果"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'}), 401

    data = request.json
    answers = data.get('answers', {})

    # 计算各维度得分
    scores = {'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0}
    for q_id, answer in answers.items():
        q_type = data.get('question_types', {}).get(q_id)
        if q_type and answer:
            scores[q_type] += 1

    # 排序得到职业代码
    sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    result_code = ''.join([t[0] for t in sorted_types[:3]])

    # 职业代码解释
    type_names = {
        'R': '实用型 (Realistic)',
        'I': '研究型 (Investigative)',
        'A': '艺术型 (Artistic)',
        'S': '社会型 (Social)',
        'E': '企业型 (Enterprising)',
        'C': '常规型 (Conventional)'
    }

    career_suggestions = {
        'R': '工程师、技术人员、机械师、建筑师、农民、飞行员',
        'I': '科学家、研究员、程序员、数据分析师、医生、药剂师',
        'A': '设计师、作家、音乐家、演员、摄影师、艺术家',
        'S': '教师、心理咨询师、护士、社会工作者、人力资源',
        'E': '销售经理、企业家、律师、政治家、市场总监',
        'C': '会计、出纳、行政人员、图书管理员、公务员'
    }

    result = {
        'code': result_code,
        'types': [type_names[t[0]] for t in sorted_types[:3]],
        'scores': scores,
        'suggestions': [career_suggestions[t[0]] for t in sorted_types[:3]]
    }

    # 保存结果
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO assessments (user_id, type, result, score)
        VALUES (?, ?, ?, ?)
    ''', (session['user_id'], 'holland', result_code, str(scores)))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'data': result})

@app.route('/api/stats')
def get_stats():
    """获取统计数据（用于后台管理）"""
    conn = get_db()
    cursor = conn.cursor()

    stats = {}

    # 用户统计
    cursor.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role")
    stats['users'] = {row['role']: row['count'] for row in cursor.fetchall()}

    # 岗位统计
    cursor.execute("SELECT COUNT(*) as count FROM internships WHERE status='active'")
    stats['internships'] = cursor.fetchone()['count']

    # 投递统计
    cursor.execute("SELECT status, COUNT(*) as count FROM applications GROUP BY status")
    stats['applications'] = {row['status']: row['count'] for row in cursor.fetchall()}

    # 文章统计
    cursor.execute("SELECT COUNT(*) as count FROM articles")
    stats['articles'] = cursor.fetchone()['count']

    # 近期投递趋势
    cursor.execute('''
        SELECT date(applied_at) as date, COUNT(*) as count
        FROM applications
        GROUP BY date(applied_at)
        ORDER BY date DESC
        LIMIT 7
    ''')
    stats['trend'] = [{'date': row['date'], 'count': row['count']} for row in cursor.fetchall()]

    conn.close()

    return jsonify({'success': True, 'data': stats})

@app.route('/admin')
def admin_page():
    """后台管理页"""
    return render_template('admin.html')

@app.route('/internships')
def internships_page():
    """实习岗位列表页"""
    return render_template('internships.html')

@app.route('/internship/<int:id>')
def internship_detail_page(id):
    """实习岗位详情页"""
    return render_template('internship_detail.html', internship_id=id)

@app.route('/resume')
def resume_page():
    """简历编辑页"""
    return render_template('resume.html')

@app.route('/articles')
def articles_page():
    """经验分享列表页"""
    return render_template('articles.html')

@app.route('/article/<int:id>')
def article_detail_page(id):
    """文章详情页"""
    return render_template('article_detail.html', article_id=id)

@app.route('/assessment')
def assessment_page():
    """职业测评页"""
    return render_template('assessment.html')

@app.route('/profile')
def profile_page():
    """个人中心页"""
    return render_template('profile.html')

if __name__ == '__main__':
    # 初始化数据库
    init_db()
    insert_sample_data()

    # 启动服务器
    print("\n" + "="*50)
    print("大学生职业规划与实习对接平台")
    print("="*50)
    print("访问地址：http://127.0.0.1:5000")
    print("\n测试账号:")
    print("  学生：student1 / 123456")
    print("  企业：hr1 / 123456")
    print("  管理：admin / 123456")
    print("="*50 + "\n")

    app.run(debug=True, port=5000)
