# 锌锭库管理系统

一个基于 Python Flask + SQLite 的锌锭库存管理系统，支持入库、出库管理，库存统计等功能。

## 功能特性

- 🔐 **用户管理**: 注册、登录、密码重置
- 📦 **入库管理**: GI锌锭入库记录管理
- 📤 **出库管理**: GI锌锭出库记录管理，支持库存校验
- 📊 **出入统计**: 独立统计页面
  - 入库统计（按年月/班组/锌锭种类）
  - 出库统计（按年月/班组/锌锭种类）
  - 当前库存统计（按锌锭种类）
- 🔍 **数据筛选**: 按日期、班组、锌锭种类筛选
- 💾 **数据导出**: 支持导出CSV格式数据
- 🏭 **高铝锌锭管理**: 独立管理高铝锌锭记录

## 系统要求

- Python 3.8 或更高版本
- 现代浏览器（Chrome、Firefox、Edge等）

## 快速开始

### Windows 系统

1. 双击运行 `start.bat` 启动脚本
2. 首次运行会自动：
   - 创建Python虚拟环境
   - 安装所需依赖
   - 初始化数据库
3. 访问 http://localhost:5000 开始使用

### 手动安装

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
python app.py
```

## 项目结构

```
锌锭库管理系统/
├── app.py              # Flask后端服务主程序
├── api.js              # 前端API通信模块
├── requirements.txt    # Python依赖包列表
├── start.bat           # Windows启动脚本
├── README.md           # 项目说明文档
├── login.html          # 登录/注册页面
├── dashboard.html      # 主管理界面（出库管理、高铝锌锭管理）
├── gi_inbound.html     # GI锌锭入库管理页面
├── gi_statistics.html  # GI锌锭出入统计页面
├── standalone/         # 纯HTML版本（无需后端）
│   ├── login.html
│   ├── dashboard.html
│   ├── gi_inbound.html
│   ├── gi_statistics.html
│   └── README.md
└── instance/
    └── zinc_management.db  # SQLite数据库文件（运行后自动生成）
```

## API 接口

### 用户接口
- `POST /api/register` - 用户注册
- `POST /api/login` - 用户登录
- `POST /api/reset-password` - 重置密码

### GI入库接口
- `GET /api/gi-inbound` - 获取所有入库记录
- `POST /api/gi-inbound` - 添加入库记录
- `PUT /api/gi-inbound/<id>` - 更新入库记录
- `DELETE /api/gi-inbound/<id>` - 删除入库记录
- `POST /api/gi-inbound/batch-delete` - 批量删除

### GI出库接口
- `GET /api/gi-outbound` - 获取所有出库记录
- `POST /api/gi-outbound` - 添加出库记录（自动校验库存）
- `PUT /api/gi-outbound/<id>` - 更新出库记录
- `DELETE /api/gi-outbound/<id>` - 删除出库记录
- `POST /api/gi-outbound/batch-delete` - 批量删除

### 高铝锌锭接口
- `GET /api/aluminum` - 获取所有记录
- `POST /api/aluminum` - 添加记录
- `PUT /api/aluminum/<id>` - 更新记录
- `DELETE /api/aluminum/<id>` - 删除记录
- `POST /api/aluminum/batch-delete` - 批量删除

### 库存统计接口
- `GET /api/stock` - 获取所有类型库存统计
- `GET /api/stock?zincType=A` - 获取指定类型库存统计

## 部署说明

### 本地部署

1. 复制整个项目文件夹到目标电脑
2. 确保目标电脑已安装 Python 3.8+
3. 运行 `start.bat` 或手动执行安装步骤

### 局域网访问

默认配置已启用局域网访问（`host='0.0.0.0'`），其他电脑可通过 `http://服务器IP:5000` 访问。

### 生产环境部署

建议使用以下方式部署：
- 使用 Gunicorn 作为 WSGI 服务器
- 使用 Nginx 作为反向代理
- 修改 `app.py` 中的 `debug=False`

## 数据安全

- 用户密码使用 Werkzeug 的安全哈希算法加密存储
- 数据存储在本地 SQLite 数据库中
- 建议定期备份 `zinc_management.db` 文件

## 常见问题

**Q: 端口被占用怎么办？**
A: 修改 `app.py` 最后一行的 `port=5000` 为其他端口号

**Q: 如何备份数据？**
A: 复制 `zinc_management.db` 文件即可

**Q: 如何重置所有数据？**
A: 删除 `zinc_management.db` 文件后重新启动服务

## 许可证

MIT License

