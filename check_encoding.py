#!/usr/bin/env python
"""
检查数据库编码和API响应
"""
import sqlite3
import requests
import json
import sys
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'career.db')

def check_db_encoding():
    """检查数据库文本编码"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("检查数据库中的文本样本...")

    # 检查实习岗位表
    cursor.execute("SELECT title, company_name, location FROM internships LIMIT 3")
    rows = cursor.fetchall()

    for i, (title, company, location) in enumerate(rows):
        print(f"岗位 {i+1}:")
        print(f"  标题: {title!r} (长度: {len(title)})")
        print(f"  公司: {company!r}")
        print(f"  地点: {location!r}")

        # 尝试检测编码（简单检查）
        try:
            title.encode('utf-8')
            print("  UTF-8编码检查: 通过")
        except UnicodeEncodeError as e:
            print(f"  UTF-8编码检查失败: {e}")

    conn.close()

def check_api_response():
    """检查API响应编码"""
    print("\n检查API响应...")
    try:
        response = requests.get('http://127.0.0.1:5000/api/internships', timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"编码: {response.encoding}")

        # 检查JSON解析
        data = response.json()
        print(f"成功解析JSON: {data.get('success')}")
        print(f"返回岗位数: {len(data.get('data', []))}")

        if data.get('data'):
            first = data['data'][0]
            print(f"第一个岗位标题: {first.get('title')!r}")
            print(f"原始字节示例: {response.content[:100]!r}")

            # 检查是否为有效UTF-8
            try:
                response.content.decode('utf-8')
                print("API响应UTF-8检查: 通过")
            except UnicodeDecodeError as e:
                print(f"API响应UTF-8检查失败: {e}")

    except Exception as e:
        print(f"检查API时出错: {e}")

def check_html_meta():
    """检查HTML页面的meta标签"""
    print("\n检查HTML页面meta标签...")
    templates = [
        'templates/index.html',
        'templates/internships.html',
        'templates/articles.html',
        'templates/assessment.html',
        'templates/profile.html'
    ]

    for tpl in templates:
        path = os.path.join(os.path.dirname(__file__), tpl)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read(1000)
                if '<meta charset="UTF-8">' in content or '<meta charset="utf-8">' in content:
                    print(f"{tpl}: 包含UTF-8 meta标签")
                else:
                    print(f"{tpl}: 缺少UTF-8 meta标签")

if __name__ == '__main__':
    check_db_encoding()
    check_api_response()
    check_html_meta()