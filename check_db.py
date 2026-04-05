#!/usr/bin/env python
"""快速检查数据库内容"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'career.db')

print(f"检查数据库: {DB_PATH}")
print("=" * 50)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 检查所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("数据库中的表:")
for table in tables:
    print(f"  - {table['name']}")
print()

# 检查每个表的数据量
for table in tables:
    table_name = table['name']
    cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
    count = cursor.fetchone()['count']
    print(f"{table_name}: {count} 条记录")

    # 如果表有数据，显示前几条
    if count > 0 and count <= 5:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        rows = cursor.fetchall()
        for i, row in enumerate(rows):
            print(f"    {i+1}. {dict(row)}")
    elif count > 5:
        print(f"    (显示前5条)")
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
        rows = cursor.fetchall()
        for i, row in enumerate(rows):
            print(f"    {i+1}. {dict(row)}")
    print()

# 特别检查用户和岗位
print("=" * 50)
print("用户表详情:")
cursor.execute("SELECT id, username, role, school, major FROM users ORDER BY id")
users = cursor.fetchall()
for user in users:
    print(f"  ID:{user['id']} 用户名:{user['username']} 角色:{user['role']} 学校:{user['school']} 专业:{user['major']}")

print("\n岗位表详情:")
cursor.execute("SELECT id, title, company_id, location, status FROM internships ORDER BY id")
internships = cursor.fetchall()
for internship in internships:
    print(f"  ID:{internship['id']} 标题:{internship['title']} 公司ID:{internship['company_id']} 地点:{internship['location']} 状态:{internship['status']}")

print("\n企业表详情:")
cursor.execute("SELECT id, company_name, industry, user_id FROM companies ORDER BY id")
companies = cursor.fetchall()
for company in companies:
    print(f"  ID:{company['id']} 名称:{company['company_name']} 行业:{company['industry']} 用户ID:{company['user_id']}")

print("\n文章表详情:")
cursor.execute("SELECT id, title, category FROM articles ORDER BY id")
articles = cursor.fetchall()
for article in articles:
    print(f"  ID:{article['id']} 标题:{article['title']} 分类:{article['category']}")

conn.close()