import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

app.post('/', (req, res) => {
  const order = req.body;
  console.log('✅ New order received:', order);

  const orderId = 'ORD' + Math.floor(Math.random() * 100000);
  res.status(200).json({ message: 'Order received', orderId });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
});
