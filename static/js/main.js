/**
 * 职引未来 - 公共 JavaScript
 */

// 检查登录状态并更新导航栏
function updateNav() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const navProfile = document.getElementById('navProfile');
    const navLogin = document.getElementById('navLogin');
    const navRegister = document.getElementById('navRegister');
    const navLogout = document.getElementById('navLogout');

    if (user && user.id) {
        if (navProfile) navProfile.style.display = 'block';
        if (navLogin) navLogin.style.display = 'none';
        if (navRegister) navRegister.style.display = 'none';
        if (navLogout) navLogout.style.display = 'block';
    } else {
        if (navProfile) navProfile.style.display = 'none';
        if (navLogin) navLogin.style.display = 'block';
        if (navRegister) navRegister.style.display = 'block';
        if (navLogout) navLogout.style.display = 'none';
    }
}

// 退出登录
async function logout() {
    if (!confirm('确定要退出登录吗？')) {
        return;
    }

    try {
        await fetch('/api/logout', { method: 'POST' });
    } catch (error) {
        console.error('登出失败');
    }

    localStorage.removeItem('user');
    window.location.href = '/';
}

// 页面加载时更新导航栏
document.addEventListener('DOMContentLoaded', () => {
    updateNav();

    // 加载首页数据
    loadHomeData();
});

// 加载首页数据
async function loadHomeData() {
    // 加载热门实习
    try {
        const response = await fetch('/api/internships');
        const data = await response.json();

        if (data.success && data.data.length > 0) {
            const hotInternships = data.data.slice(0, 4);
            let html = '<div class="list-group">';
            hotInternships.forEach(item => {
                html += `
                    <a href="/internship/${item.id}" class="list-group-item list-group-item-action">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">${item.title}</h5>
                            <span class="text-primary fw-bold">${item.salary}</span>
                        </div>
                        <p class="mb-1">
                            <span class="badge bg-primary">${item.company_name}</span>
                            <span class="badge bg-secondary">${item.location}</span>
                        </p>
                    </a>
                `;
            });
            html += '</div>';
            const container = document.getElementById('hotInternships');
            if (container) container.innerHTML = html;
        }
    } catch (error) {
        console.error('加载实习岗位失败');
    }

    // 加载最新文章
    try {
        const response = await fetch('/api/articles');
        const data = await response.json();

        if (data.success && data.data.length > 0) {
            const latestArticles = data.data.slice(0, 3);
            let html = '<div class="row">';
            latestArticles.forEach(article => {
                html += `
                    <div class="col-md-4 mb-3">
                        <div class="card h-100">
                            <div class="card-body">
                                <span class="badge bg-secondary mb-2">${article.category || '其他'}</span>
                                <h5 class="card-title">${article.title}</h5>
                                <p class="card-text text-muted small">${article.content?.substring(0, 80)}...</p>
                            </div>
                            <div class="card-footer bg-white">
                                <a href="/article/${article.id}" class="btn btn-sm btn-outline-primary">阅读全文</a>
                            </div>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            const container = document.getElementById('latestArticles');
            if (container) container.innerHTML = html;
        }
    } catch (error) {
        console.error('加载文章失败');
    }

    // 加载统计数据
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        if (data.success) {
            const stats = data.data;
            const companiesEl = document.getElementById('statCompanies');
            const internshipsEl = document.getElementById('statInternships');
            const studentsEl = document.getElementById('statStudents');
            const articlesEl = document.getElementById('statArticles');

            if (companiesEl) companiesEl.textContent = (stats.users.enterprise || 0) + 4;
            if (internshipsEl) internshipsEl.textContent = stats.internships || 0;
            if (studentsEl) studentsEl.textContent = (stats.users.student || 0) + 100;
            if (articlesEl) articlesEl.textContent = stats.articles || 0;
        }
    } catch (error) {
        console.error('加载统计失败');
    }
}

// 表单验证辅助函数
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let valid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            valid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return valid;
}

// 显示提示信息
function showMessage(elementId, message, type = 'info') {
    const el = document.getElementById(elementId);
    if (!el) return;

    el.className = `alert alert-${type}`;
    el.textContent = message;
    el.style.display = 'block';

    setTimeout(() => {
        el.style.display = 'none';
    }, 3000);
}

// 日期格式化
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

// 本地存储辅助
const storage = {
    get: (key) => {
        try {
            return JSON.parse(localStorage.getItem(key));
        } catch {
            return null;
        }
    },
    set: (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    },
    remove: (key) => {
        localStorage.removeItem(key);
    }
};
