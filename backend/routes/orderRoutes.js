const express = require('express');
const {
  createOrder,
  getUserOrders,
  getOrder,
  updateOrderStatus,
  handlePaymentCallback
} = require('../controllers/orderController');
const { protect } = require('../middlewares/auth');

const router = express.Router();

// Public routes (anyone can create an order without authentication)
router.post('/', createOrder);

// Payment callback route (typically called by payment gateway)
router.post('/payment/callback', handlePaymentCallback);

// Protected routes
router.get('/user', protect, getUserOrders);
router.get('/:id', protect, getOrder);
router.put('/:id/status', protect, updateOrderStatus);

module.exports = router;