import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

let orders = []; // In-memory order store

app.post('/', (req, res) => {
  const order = req.body;
  const orderId = 'ORD' + Math.floor(Math.random() * 100000);
  order.orderId = orderId;
  order.timestamp = new Date().toISOString();
  orders.push(order);

  console.log('✅ New order received:', order);
  res.status(200).json({ message: 'Order received', orderId });
});

// ✅ GET endpoint for admin GUI
app.get('/orders', (req, res) => {
  res.json(orders);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
});
