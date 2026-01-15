# -*- coding: utf-8 -*-
"""
锌锭库管理系统 - 后端服务
使用Flask框架和SQLite数据库
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# 创建Flask应用
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # 允许跨域请求

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zinc_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)


# ==================== 数据库模型 ====================

class User(db.Model):
    """用户表"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class GiInbound(db.Model):
    """GI锌锭入库记录表"""
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(10), nullable=False)  # 班组：甲、乙、丙、丁
    zinc_type = db.Column(db.String(10), nullable=False)  # 锌锭种类：A、B、D、E
    quantity = db.Column(db.Integer, nullable=False)  # 入库数量
    weight = db.Column(db.Float, nullable=False)  # 入库重量(KG)
    date = db.Column(db.DateTime, nullable=False)  # 入库时间
    field_e = db.Column(db.String(100))  # E字段
    field_f = db.Column(db.String(100))  # F字段
    field_g = db.Column(db.String(100))  # G字段
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'A': self.team,
            'ZincType': self.zinc_type,
            'B': str(self.quantity),
            'C': str(self.weight),
            'D': self.date.isoformat() if self.date else '',
            'E': self.field_e or '',
            'F': self.field_f or '',
            'G': self.field_g or '',
            'selected': False
        }


class GiOutbound(db.Model):
    """GI锌锭出库记录表"""
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(10), nullable=False)  # 班组
    zinc_type = db.Column(db.String(10), nullable=False)  # 锌锭种类
    quantity = db.Column(db.Integer, nullable=False)  # 出库数量
    weight = db.Column(db.Float, nullable=False)  # 出库重量(KG)
    date = db.Column(db.DateTime, nullable=False)  # 出库时间
    field_e = db.Column(db.String(100))
    field_f = db.Column(db.String(100))
    field_g = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'A': self.team,
            'ZincType': self.zinc_type,
            'B': str(self.quantity),
            'C': str(self.weight),
            'D': self.date.isoformat() if self.date else '',
            'E': self.field_e or '',
            'F': self.field_f or '',
            'G': self.field_g or '',
            'selected': False
        }


class AluminumZinc(db.Model):
    """高铝锌锭记录表"""
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(10), nullable=False)  # 班组
    quantity = db.Column(db.Integer, nullable=False)  # 数量
    weight = db.Column(db.Float, nullable=False)  # 重量(KG)
    date = db.Column(db.DateTime, nullable=False)  # 消耗时间
    field_e = db.Column(db.String(100))
    field_f = db.Column(db.String(100))
    field_g = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'A': self.team,
            'B': str(self.quantity),
            'C': str(self.weight),
            'D': self.date.isoformat() if self.date else '',
            'E': self.field_e or '',
            'F': self.field_f or '',
            'G': self.field_g or '',
            'selected': False
        }


# ==================== 静态文件路由 ====================

@app.route('/')
def index():
    return send_from_directory('.', 'login.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


# ==================== 用户API ====================

@app.route('/api/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    # 验证输入
    if not username or not email or not password:
        return jsonify({'success': False, 'message': '请填写所有字段'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'message': '密码至少需要6位'}), 400

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': '该账号已被注册'}), 400

    # 检查邮箱是否已存在
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': '该邮箱已被注册'}), 400

    # 创建新用户
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'success': True, 'message': '注册成功'})


@app.route('/api/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': '账号或密码错误'}), 401

    return jsonify({
        'success': True,
        'message': '登录成功',
        'user': user.to_dict()
    })


@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    """重置密码"""
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    new_password = data.get('newPassword', '')

    if len(new_password) < 6:
        return jsonify({'success': False, 'message': '密码至少需要6位'}), 400

    user = User.query.filter_by(username=username, email=email).first()

    if not user:
        return jsonify({'success': False, 'message': '账号或邮箱不匹配'}), 404

    user.set_password(new_password)
    db.session.commit()

    return jsonify({'success': True, 'message': '密码重置成功'})


# ==================== GI入库API ====================

@app.route('/api/gi-inbound', methods=['GET'])
def get_gi_inbound():
    """获取所有GI入库记录（按时间升序排序）"""
    records = GiInbound.query.order_by(GiInbound.date.asc()).all()
    return jsonify({'success': True, 'data': [r.to_dict() for r in records]})


@app.route('/api/gi-inbound', methods=['POST'])
def add_gi_inbound():
    """添加GI入库记录"""
    data = request.get_json()
    
    record = GiInbound(
        team=data.get('A', ''),
        zinc_type=data.get('ZincType', ''),
        quantity=int(data.get('B', 0)),
        weight=float(data.get('C', 0)),
        date=datetime.strptime(data.get('D', ''), '%Y-%m-%dT%H:%M') if data.get('D') else None,
        field_e=data.get('E', ''),
        field_f=data.get('F', ''),
        field_g=data.get('G', '')
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({'success': True, 'data': record.to_dict()})


@app.route('/api/gi-inbound/<int:id>', methods=['PUT'])
def update_gi_inbound(id):
    """更新GI入库记录"""
    record = GiInbound.query.get_or_404(id)
    data = request.get_json()
    
    record.team = data.get('A', record.team)
    record.zinc_type = data.get('ZincType', record.zinc_type)
    record.quantity = int(data.get('B', record.quantity))
    record.weight = float(data.get('C', record.weight))
    if data.get('D'):
        record.date = datetime.strptime(data.get('D'), '%Y-%m-%dT%H:%M')
    record.field_e = data.get('E', record.field_e)
    record.field_f = data.get('F', record.field_f)
    record.field_g = data.get('G', record.field_g)
    
    db.session.commit()
    
    return jsonify({'success': True, 'data': record.to_dict()})


@app.route('/api/gi-inbound/<int:id>', methods=['DELETE'])
def delete_gi_inbound(id):
    """删除GI入库记录"""
    record = GiInbound.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '删除成功'})


@app.route('/api/gi-inbound/batch-delete', methods=['POST'])
def batch_delete_gi_inbound():
    """批量删除GI入库记录"""
    data = request.get_json()
    ids = data.get('ids', [])
    
    GiInbound.query.filter(GiInbound.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'成功删除{len(ids)}条记录'})


# ==================== GI出库API ====================

@app.route('/api/gi-outbound', methods=['GET'])
def get_gi_outbound():
    """获取所有GI出库记录（按时间升序排序）"""
    records = GiOutbound.query.order_by(GiOutbound.date.asc()).all()
    return jsonify({'success': True, 'data': [r.to_dict() for r in records]})


@app.route('/api/gi-outbound', methods=['POST'])
def add_gi_outbound():
    """添加GI出库记录"""
    data = request.get_json()
    zinc_type = data.get('ZincType', '')
    quantity = int(data.get('B', 0))
    weight = float(data.get('C', 0))
    
    # 检查库存
    stock = get_stock_by_type(zinc_type)
    if quantity > stock['remaining_quantity']:
        return jsonify({
            'success': False,
            'message': f'出库失败，库存不足！锌锭种类 {zinc_type} 的剩余数量为 {stock["remaining_quantity"]} 个，您尝试出库 {quantity} 个。'
        }), 400
    
    if weight > stock['remaining_weight']:
        return jsonify({
            'success': False,
            'message': f'出库失败，库存不足！锌锭种类 {zinc_type} 的剩余重量为 {stock["remaining_weight"]} KG，您尝试出库 {weight} KG。'
        }), 400
    
    record = GiOutbound(
        team=data.get('A', ''),
        zinc_type=zinc_type,
        quantity=quantity,
        weight=weight,
        date=datetime.strptime(data.get('D', ''), '%Y-%m-%dT%H:%M') if data.get('D') else None,
        field_e=data.get('E', ''),
        field_f=data.get('F', ''),
        field_g=data.get('G', '')
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({'success': True, 'data': record.to_dict()})


@app.route('/api/gi-outbound/<int:id>', methods=['PUT'])
def update_gi_outbound(id):
    """更新GI出库记录"""
    record = GiOutbound.query.get_or_404(id)
    data = request.get_json()
    zinc_type = data.get('ZincType', record.zinc_type)
    quantity = int(data.get('B', record.quantity))
    weight = float(data.get('C', record.weight))
    
    # 检查库存（排除当前记录）
    stock = get_stock_by_type(zinc_type, exclude_outbound_id=id)
    if quantity > stock['remaining_quantity']:
        return jsonify({
            'success': False,
            'message': f'出库失败，库存不足！锌锭种类 {zinc_type} 的剩余数量为 {stock["remaining_quantity"]} 个，您尝试出库 {quantity} 个。'
        }), 400
    
    if weight > stock['remaining_weight']:
        return jsonify({
            'success': False,
            'message': f'出库失败，库存不足！锌锭种类 {zinc_type} 的剩余重量为 {stock["remaining_weight"]} KG，您尝试出库 {weight} KG。'
        }), 400
    
    record.team = data.get('A', record.team)
    record.zinc_type = zinc_type
    record.quantity = quantity
    record.weight = weight
    if data.get('D'):
        record.date = datetime.strptime(data.get('D'), '%Y-%m-%dT%H:%M')
    record.field_e = data.get('E', record.field_e)
    record.field_f = data.get('F', record.field_f)
    record.field_g = data.get('G', record.field_g)
    
    db.session.commit()
    
    return jsonify({'success': True, 'data': record.to_dict()})


@app.route('/api/gi-outbound/<int:id>', methods=['DELETE'])
def delete_gi_outbound(id):
    """删除GI出库记录"""
    record = GiOutbound.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '删除成功'})


@app.route('/api/gi-outbound/batch-delete', methods=['POST'])
def batch_delete_gi_outbound():
    """批量删除GI出库记录"""
    data = request.get_json()
    ids = data.get('ids', [])
    
    GiOutbound.query.filter(GiOutbound.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'成功删除{len(ids)}条记录'})


# ==================== 高铝锌锭API ====================

@app.route('/api/aluminum', methods=['GET'])
def get_aluminum():
    """获取所有高铝锌锭记录（按时间升序排序）"""
    records = AluminumZinc.query.order_by(AluminumZinc.date.asc()).all()
    return jsonify({'success': True, 'data': [r.to_dict() for r in records]})


@app.route('/api/aluminum', methods=['POST'])
def add_aluminum():
    """添加高铝锌锭记录"""
    data = request.get_json()
    
    record = AluminumZinc(
        team=data.get('A', ''),
        quantity=int(data.get('B', 0)),
        weight=float(data.get('C', 0)),
        date=datetime.strptime(data.get('D', ''), '%Y-%m-%dT%H:%M') if data.get('D') else None,
        field_e=data.get('E', ''),
        field_f=data.get('F', ''),
        field_g=data.get('G', '')
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({'success': True, 'data': record.to_dict()})


@app.route('/api/aluminum/<int:id>', methods=['PUT'])
def update_aluminum(id):
    """更新高铝锌锭记录"""
    record = AluminumZinc.query.get_or_404(id)
    data = request.get_json()
    
    record.team = data.get('A', record.team)
    record.quantity = int(data.get('B', record.quantity))
    record.weight = float(data.get('C', record.weight))
    if data.get('D'):
        record.date = datetime.strptime(data.get('D'), '%Y-%m-%dT%H:%M')
    record.field_e = data.get('E', record.field_e)
    record.field_f = data.get('F', record.field_f)
    record.field_g = data.get('G', record.field_g)
    
    db.session.commit()
    
    return jsonify({'success': True, 'data': record.to_dict()})


@app.route('/api/aluminum/<int:id>', methods=['DELETE'])
def delete_aluminum(id):
    """删除高铝锌锭记录"""
    record = AluminumZinc.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '删除成功'})


@app.route('/api/aluminum/batch-delete', methods=['POST'])
def batch_delete_aluminum():
    """批量删除高铝锌锭记录"""
    data = request.get_json()
    ids = data.get('ids', [])
    
    AluminumZinc.query.filter(AluminumZinc.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'成功删除{len(ids)}条记录'})


# ==================== 库存统计API ====================

def get_stock_by_type(zinc_type, exclude_outbound_id=None):
    """获取指定锌锭种类的库存"""
    # 入库总量
    inbound_query = db.session.query(
        db.func.coalesce(db.func.sum(GiInbound.quantity), 0),
        db.func.coalesce(db.func.sum(GiInbound.weight), 0)
    ).filter(GiInbound.zinc_type == zinc_type)
    inbound_result = inbound_query.first()
    inbound_quantity = inbound_result[0]
    inbound_weight = inbound_result[1]
    
    # 出库总量
    outbound_query = db.session.query(
        db.func.coalesce(db.func.sum(GiOutbound.quantity), 0),
        db.func.coalesce(db.func.sum(GiOutbound.weight), 0)
    ).filter(GiOutbound.zinc_type == zinc_type)
    
    if exclude_outbound_id:
        outbound_query = outbound_query.filter(GiOutbound.id != exclude_outbound_id)
    
    outbound_result = outbound_query.first()
    outbound_quantity = outbound_result[0]
    outbound_weight = outbound_result[1]
    
    return {
        'inbound_quantity': inbound_quantity,
        'inbound_weight': inbound_weight,
        'outbound_quantity': outbound_quantity,
        'outbound_weight': outbound_weight,
        'remaining_quantity': inbound_quantity - outbound_quantity,
        'remaining_weight': inbound_weight - outbound_weight
    }


@app.route('/api/stock', methods=['GET'])
def get_stock():
    """获取库存统计"""
    zinc_type = request.args.get('zincType', '')
    
    if zinc_type:
        # 获取指定类型的库存
        stock = get_stock_by_type(zinc_type)
        return jsonify({'success': True, 'data': stock})
    else:
        # 获取所有类型的库存
        result = {}
        for t in ['A', 'B', 'C', 'D']:
            result[t] = get_stock_by_type(t)
        
        # 计算总计
        total = {
            'inbound_quantity': sum(r['inbound_quantity'] for r in result.values()),
            'inbound_weight': sum(r['inbound_weight'] for r in result.values()),
            'outbound_quantity': sum(r['outbound_quantity'] for r in result.values()),
            'outbound_weight': sum(r['outbound_weight'] for r in result.values()),
            'remaining_quantity': sum(r['remaining_quantity'] for r in result.values()),
            'remaining_weight': sum(r['remaining_weight'] for r in result.values())
        }
        result['total'] = total
        
        return jsonify({'success': True, 'data': result})


# ==================== 初始化数据库 ====================

def init_db():
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        print("数据库初始化完成！")


# ==================== 启动服务 ====================

if __name__ == '__main__':
    # 初始化数据库
    init_db()
    
    print("=" * 50)
    print("锌锭库管理系统 - 后端服务已启动")
    print("=" * 50)
    print("访问地址: http://localhost:5000")
    print("登录页面: http://localhost:5000/login.html")
    print("=" * 50)
    
    # 启动服务（debug=True 用于开发，生产环境应设为False）
    app.run(host='0.0.0.0', port=5000, debug=True)

