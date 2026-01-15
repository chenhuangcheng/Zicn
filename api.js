/**
 * 锌锭库管理系统 - API通信模块
 * 统一管理前后端通信
 */

const API_BASE_URL = '';  // 同域部署，无需前缀

// ==================== 通用请求方法 ====================

async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(API_BASE_URL + url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || '请求失败');
        }
        
        return result;
    } catch (error) {
        console.error('API请求错误:', error);
        throw error;
    }
}

// ==================== 用户相关API ====================

const UserAPI = {
    // 用户注册
    async register(username, email, password) {
        return await apiRequest('/api/register', 'POST', { username, email, password });
    },
    
    // 用户登录
    async login(username, password) {
        return await apiRequest('/api/login', 'POST', { username, password });
    },
    
    // 重置密码
    async resetPassword(username, email, newPassword) {
        return await apiRequest('/api/reset-password', 'POST', { username, email, newPassword });
    }
};

// ==================== GI入库API ====================

const GiInboundAPI = {
    // 获取所有入库记录
    async getAll() {
        const result = await apiRequest('/api/gi-inbound');
        return result.data || [];
    },
    
    // 添加入库记录
    async add(data) {
        return await apiRequest('/api/gi-inbound', 'POST', data);
    },
    
    // 更新入库记录
    async update(id, data) {
        return await apiRequest(`/api/gi-inbound/${id}`, 'PUT', data);
    },
    
    // 删除入库记录
    async delete(id) {
        return await apiRequest(`/api/gi-inbound/${id}`, 'DELETE');
    },
    
    // 批量删除入库记录
    async batchDelete(ids) {
        return await apiRequest('/api/gi-inbound/batch-delete', 'POST', { ids });
    }
};

// ==================== GI出库API ====================

const GiOutboundAPI = {
    // 获取所有出库记录
    async getAll() {
        const result = await apiRequest('/api/gi-outbound');
        return result.data || [];
    },
    
    // 添加出库记录
    async add(data) {
        return await apiRequest('/api/gi-outbound', 'POST', data);
    },
    
    // 更新出库记录
    async update(id, data) {
        return await apiRequest(`/api/gi-outbound/${id}`, 'PUT', data);
    },
    
    // 删除出库记录
    async delete(id) {
        return await apiRequest(`/api/gi-outbound/${id}`, 'DELETE');
    },
    
    // 批量删除出库记录
    async batchDelete(ids) {
        return await apiRequest('/api/gi-outbound/batch-delete', 'POST', { ids });
    }
};

// ==================== 高铝锌锭API ====================

const AluminumAPI = {
    // 获取所有记录
    async getAll() {
        const result = await apiRequest('/api/aluminum');
        return result.data || [];
    },
    
    // 添加记录
    async add(data) {
        return await apiRequest('/api/aluminum', 'POST', data);
    },
    
    // 更新记录
    async update(id, data) {
        return await apiRequest(`/api/aluminum/${id}`, 'PUT', data);
    },
    
    // 删除记录
    async delete(id) {
        return await apiRequest(`/api/aluminum/${id}`, 'DELETE');
    },
    
    // 批量删除记录
    async batchDelete(ids) {
        return await apiRequest('/api/aluminum/batch-delete', 'POST', { ids });
    }
};

// ==================== 库存统计API ====================

const StockAPI = {
    // 获取库存统计
    async getStock(zincType = '') {
        const url = zincType ? `/api/stock?zincType=${zincType}` : '/api/stock';
        const result = await apiRequest(url);
        return result.data;
    }
};

