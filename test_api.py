#!/usr/bin/env python
"""测试API是否返回数据"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("测试API数据返回...")
print("=" * 50)

try:
    # 1. 测试岗位API
    print("1. 测试实习岗位API...")
    response = requests.get(f"{BASE_URL}/api/internships")
    if response.status_code == 200:
        data = response.json()
        print(f"   状态: 成功")
        print(f"   返回岗位数量: {len(data.get('data', []))}")
        if data.get('data'):
            for i, internship in enumerate(data.get('data')[:3]):
                print(f"   岗位{i+1}: {internship.get('title')} - {internship.get('company_name')}")
    else:
        print(f"   状态: 失败 ({response.status_code})")

    # 2. 测试文章API
    print("\n2. 测试经验分享API...")
    response = requests.get(f"{BASE_URL}/api/articles")
    if response.status_code == 200:
        data = response.json()
        print(f"   状态: 成功")
        print(f"   返回文章数量: {len(data.get('data', []))}")
        if data.get('data'):
            for i, article in enumerate(data.get('data')[:3]):
                print(f"   文章{i+1}: {article.get('title')} - {article.get('category')}")
    else:
        print(f"   状态: 失败 ({response.status_code})")

    # 3. 测试企业API（通过岗位查询间接测试）
    print("\n3. 测试企业数据...")
    response = requests.get(f"{BASE_URL}/api/internships")
    if response.status_code == 200:
        data = response.json()
        companies = set()
        for internship in data.get('data', []):
            companies.add(internship.get('company_name', ''))
        print(f"   状态: 成功")
        print(f"   涉及企业数量: {len(companies)}")
        if companies:
            print(f"   企业列表: {', '.join(list(companies)[:5])}{'...' if len(companies) > 5 else ''}")

    # 4. 测试登录（使用测试账号）
    print("\n4. 测试登录功能...")
    login_data = {"username": "student1", "password": "123456"}
    response = requests.post(f"{BASE_URL}/api/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        print(f"   状态: 成功")
        print(f"   用户: {data.get('username')}")
        print(f"   角色: {data.get('role')}")

        # 测试获取推荐（需要session，这里只测试接口）
        print("\n5. 测试推荐接口（需要登录后的cookie）...")
        print("   请手动在浏览器中测试: /api/recommendations")
    else:
        print(f"   状态: 失败 ({response.status_code})")
        print(f"   错误: {response.text}")

    print("\n" + "=" * 50)
    print("测试完成！如果上述测试显示有数据，则数据库修复成功。")
    print("如果仍然看不到数据，可能是前端缓存问题，请尝试：")
    print("1. 清除浏览器缓存")
    print("2. 使用隐身模式访问")
    print("3. 按Ctrl+F5强制刷新页面")

except requests.exceptions.ConnectionError:
    print("错误: 无法连接到服务器，请确保应用正在运行！")
    print("运行命令: python app.py")
except Exception as e:
    print(f"错误: {e}")