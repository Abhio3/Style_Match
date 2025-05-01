const express = require('express');
const {
  getDashboardStats,
  getAllUsers,
  getAllAppointments,
  getAllOrders,
  getAllProducts,
  addProduct,
  updateProduct,
  deleteProduct
} = require('../controllers/adminController');
const { protect, authorize } = require('../middlewares/auth');
const config = require('../config/config');

const router = express.Router();

// Admin routes (all routes are protected and require admin role)
router.use(protect);
router.use(authorize(config.roles.ADMIN));

// Dashboard statistics
router.get('/dashboard', getDashboardStats);

// User management
router.get('/users', getAllUsers);

// Appointment management
router.get('/appointments', getAllAppointments);

// Order management
router.get('/orders', getAllOrders);

// Product management
router.get('/products', getAllProducts);
router.post('/products', addProduct);
router.put('/products/:id', updateProduct);
router.delete('/products/:id', deleteProduct);

module.exports = router;