from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS # For handling Cross-Origin Resource Sharing

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# --- Database Configuration ---
# Use SQLite, a file-based database. 'site.db' will be created in your project folder.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Suppress a warning

db = SQLAlchemy(app)

# --- Define the Order Model (Database Table Structure) ---
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    google_pay_name = db.Column(db.String(100), default='')
    transaction_id = db.Column(db.String(100), default='')
    items = db.Column(db.JSON, nullable=False) # Store cart items as JSON
    total_price = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Order('{self.id}', '{self.contact_name}', '{self.order_date}')"

# --- API Route to Receive Orders ---
@app.route('/api/orders', methods=['POST'])
def place_order():
    try:
        data = request.get_json()

        # Basic validation (add more as needed)
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        if not all(k in data for k in ['contactName', 'address', 'phoneNumber', 'paymentMethod', 'items', 'totalPrice']):
            return jsonify({'message': 'Missing required order fields'}), 400
        if not isinstance(data['items'], list) or not data['items']:
            return jsonify({'message': 'Order must contain items'}), 400
        if not isinstance(data['totalPrice'], (int, float)) or data['totalPrice'] <= 0:
            return jsonify({'message': 'Invalid total price'}), 400

        new_order = Order(
            contact_name=data['contactName'],
            address=data['address'],
            phone_number=data['phoneNumber'],
            payment_method=data['paymentMethod'],
            google_pay_name=data.get('googlePayName', ''),
            transaction_id=data.get('transactionId', ''),
            items=data['items'], # SQLAlchemy handles JSON for SQLite
            total_price=data['totalPrice']
        )

        db.session.add(new_order)
        db.session.commit()

        print(f"Order saved to database: {new_order.id}")
        return jsonify({'message': 'Order received and saved successfully!', 'orderId': new_order.id}), 201

    except Exception as e:
        print(f"Error saving order: {e}")
        return jsonify({'message': 'Failed to save order.', 'error': str(e)}), 500

# Optional: A route to fetch all orders (for testing/admin view)
@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.all()
        orders_list = []
        for order in orders:
            orders_list.append({
                'id': order.id,
                'contactName': order.contact_name,
                'address': order.address,
                'phoneNumber': order.phone_number,
                'paymentMethod': order.payment_method,
                'googlePayName': order.google_pay_name,
                'transactionId': order.transaction_id,
                'items': order.items,
                'totalPrice': order.total_price,
                'orderDate': order.order_date.isoformat()
            })
        return jsonify(orders_list), 200
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return jsonify({'message': 'Failed to fetch orders.', 'error': str(e)}), 500

if __name__ == '__main__':
    # Create database tables before running the app
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000) # debug=True enables auto-reloading and better error messages