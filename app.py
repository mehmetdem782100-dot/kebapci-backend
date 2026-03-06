from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Dosya yolları
PRODUCTS_FILE = 'products.json'
ORDERS_FILE = os.path.join('data', 'orders.json')

# Eğer orders.json yoksa oluştur
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, 'w') as f:
        json.dump([], f)

# Ana sayfa (müşteri)
@app.route('/admin')
def admin():
    token = request.args.get('token', '')
    if token != os.environ.get('ADMIN_TOKEN', 'Helin7878+'):
        return "Unauthorized", 401
    return render_template('admin.html')

# Admin panel
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Ürünleri listele
@app.route('/api/products', methods=['GET'])
def get_products():
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        products = json.load(f)
    return jsonify(products)

# Sipariş ekle
@app.route('/api/orders', methods=['POST'])
def add_order():
    data = request.json
    with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
        orders = json.load(f)
    order_id = len(orders) + 1
    order = {
        "order_id": order_id,
        "name": data.get('name'),
        "phone": data.get('phone'),
        "address": data.get('address'),
        "items": data.get('items')
    }
    orders.append(order)
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    return jsonify({"ok": True, "order_id": order_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)