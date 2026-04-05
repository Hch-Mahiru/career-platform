/**
 * 职引未来 - 公共 JavaScript
 */

// 检查登录状态并更新导航栏
function updateNav() {
    try {
        let user = {};
        try {
            user = JSON.parse(localStorage.getItem('user') || '{}');
        } catch (e) {
            console.warn('解析用户信息失败，清空 localStorage');
            localStorage.removeItem('user');
        }

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
    } catch (error) {
        console.error('更新导航栏时出错:', error);
    }
}

// 简单的HTML转义函数（防止XSS和模板字符串中断）
function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
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
                // 转义动态内容
                const title = escapeHtml(item.title || '');
                const salary = escapeHtml(item.salary || '');
                const company = escapeHtml(item.company_name || '');
                const location = escapeHtml(item.location || '');

                html += `
                    <a href="/internship/${item.id}" class="list-group-item list-group-item-action">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">${title}</h5>
                            <span class="text-primary fw-bold">${salary}</span>
                        </div>
                        <p class="mb-1">
                            <span class="badge bg-primary">${company}</span>
                            <span class="badge bg-secondary">${location}</span>
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
                // 转义动态内容
                const category = escapeHtml(article.category || '其他');
                const title = escapeHtml(article.title || '');
                const content = escapeHtml((article.content || '').substring(0, 80));

                html += `
                    <div class="col-md-4 mb-3">
                        <div class="card h-100">
                            <div class="card-body">
                                <span class="badge bg-secondary mb-2">${category}</span>
                                <h5 class="card-title">${title}</h5>
                                <p class="card-text text-muted small">${content}...</p>
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

// ==================== 智能推荐功能 ====================

// 加载个性化岗位推荐
async function loadRecommendations() {
    const loadingEl = document.getElementById('recommendationsLoading');
    const listEl = document.getElementById('recommendationsList');
    const noRecEl = document.getElementById('noRecommendations');

    if (!loadingEl || !listEl || !noRecEl) {
        alert('推荐功能未正确初始化');
        return;
    }

    // 显示加载状态
    loadingEl.classList.remove('d-none');
    listEl.classList.add('d-none');
    noRecEl.classList.add('d-none');

    try {
        // 添加超时机制（8秒）
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 8000);

        const response = await fetch('/api/recommendations?limit=10', {
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        const data = await response.json();

        if (data.success && data.data.length > 0) {
            let html = '<div class="list-group">';
            data.data.forEach(item => {
                const score = item.match_score || 0;
                const reasons = item.recommendation_reasons || [];
                const type = item.recommendation_type || 'content_based';

                html += `
                    <div class="list-group-item list-group-item-action">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">${item.title}</h5>
                            <div>
                                <span class="badge bg-success">匹配度 ${score}%</span>
                                <span class="badge bg-info ms-1">${type === 'content_based' ? '内容推荐' : '协同过滤'}</span>
                            </div>
                        </div>
                        <p class="mb-1">
                            <span class="badge bg-primary">${item.company_name}</span>
                            <span class="badge bg-secondary">${item.location}</span>
                            <span class="badge bg-warning">${item.salary}</span>
                        </p>
                        <p class="mb-1 small">${item.description}</p>
                        ${reasons.length > 0 ? `
                            <div class="mt-2">
                                <small class="text-muted">推荐理由：</small>
                                <ul class="small mb-0">
                                    ${reasons.map(reason => `<li>${reason}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                        <div class="mt-2 d-flex gap-2">
                            <a href="/internship/${item.id}" class="btn btn-sm btn-outline-primary">查看详情</a>
                            <button class="btn btn-sm btn-success" onclick="applyForInternship(${item.id})">立即投递</button>
                        </div>
                    </div>
                `;
            });
            html += '</div>';

            listEl.innerHTML = html;
            loadingEl.classList.add('d-none');
            listEl.classList.remove('d-none');
        } else {
            loadingEl.classList.add('d-none');
            noRecEl.classList.remove('d-none');
        }
    } catch (error) {
        console.error('加载推荐失败:', error);
        loadingEl.classList.add('d-none');

        if (error.name === 'AbortError') {
            alert('加载推荐超时，请稍后再试或联系管理员');
        } else {
            alert('加载推荐失败，请检查网络连接或登录状态');
        }
    }
}

// 解释推荐算法原理
async function explainRecommendations() {
    try {
        const response = await fetch('/api/recommendations/explain');
        const data = await response.json();

        if (data.success) {
            let message = `<strong>${data.algorithm}</strong><br>${data.description}<br><br>`;
            message += '<strong>推荐因素：</strong><ul>';
            data.factors.forEach(factor => {
                message += `<li>${factor.name} (${factor.weight}): ${factor.description}</li>`;
            });
            message += '</ul><strong>数据来源：</strong><ul>';
            data.data_sources.forEach(source => {
                message += `<li>${source}</li>`;
            });
            message += `</ul><strong>实现方式：</strong> ${data.implementation}`;

            alertWithHtml(message);
        }
    } catch (error) {
        console.error('获取算法解释失败:', error);
        alert('获取推荐原理失败');
    }
}

// 使用HTML内容的alert替代函数
function alertWithHtml(html) {
    const modalHtml = `
        <div class="modal fade" id="recommendationExplainModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">推荐算法原理</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${html}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // 移除现有模态框
    const existingModal = document.getElementById('recommendationExplainModal');
    if (existingModal) {
        existingModal.remove();
    }

    // 添加新模态框
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('recommendationExplainModal'));
    modal.show();
}

// 投递岗位函数（需在页面中实现）
function applyForInternship(internshipId) {
    if (!confirm('确定投递该岗位吗？')) return;

    fetch('/api/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ internship_id: internshipId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('投递成功！');
            // 刷新推荐列表，避免重复推荐
            loadRecommendations();
        } else {
            alert(`投递失败：${data.message}`);
        }
    })
    .catch(error => {
        console.error('投递失败:', error);
        alert('网络错误，请重试');
    });
}

// 页面加载时，如果处于推荐标签页，自动加载推荐
document.addEventListener('DOMContentLoaded', () => {
    // 检查当前是否在推荐标签页
    const activeSection = document.querySelector('.list-group-item.active');
    if (activeSection && activeSection.dataset.section === 'recommendations') {
        loadRecommendations();
    }
});
