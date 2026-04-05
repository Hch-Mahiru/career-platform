#!/usr/bin/env python
"""
修复实习岗位与公司ID不匹配的问题
运行: python fix_data.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'career.db')

def fix_company_ids():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("检查当前数据...")
    cursor.execute('SELECT COUNT(*) FROM internships')
    total_internships = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM companies')
    total_companies = cursor.fetchone()[0]
    print(f"实习岗位数: {total_internships}, 公司数: {total_companies}")

    # 检查不匹配的记录
    cursor.execute('''
        SELECT i.id, i.company_id, c.id as real_company_id
        FROM internships i
        LEFT JOIN companies c ON i.company_id = c.id
        WHERE c.id IS NULL
    ''')
    mismatched = cursor.fetchall()
    print(f"发现 {len(mismatched)} 个不匹配的实习岗位")

    if not mismatched:
        print("数据已匹配，无需修复。")
        conn.close()
        return

    # 计算偏移量（假设公司ID从17开始）
    cursor.execute('SELECT MIN(id) FROM companies')
    min_company_id = cursor.fetchone()[0]
    offset = min_company_id - 1

    print(f"检测到公司ID最小值为 {min_company_id}，将应用偏移量 +{offset}")

    # 更新实习岗位的company_id
    cursor.execute('''
        UPDATE internships
        SET company_id = company_id + ?
        WHERE company_id BETWEEN 1 AND 12
    ''', (offset,))

    conn.commit()

    # 验证修复
    cursor.execute('''
        SELECT COUNT(*)
        FROM internships i
        JOIN companies c ON i.company_id = c.id
    ''')
    matched_count = cursor.fetchone()[0]
    print(f"修复后匹配的实习岗位数: {matched_count}/{total_internships}")

    conn.close()

    if matched_count == total_internships:
        print("[成功] 数据修复成功！API现在应能返回所有岗位。")
    else:
        print("[警告] 仍有部分岗位未匹配，请检查数据完整性。")

if __name__ == '__main__':
    fix_company_ids()