const User = require('../models/User');
const Appointment = require('../models/Appointment');
const BridalService = require('../models/BridalService');
const { Order, OrderItem } = require('../models/Order');
const Product = require('../models/Product');
const { sequelize } = require('../config/database');
const { Op } = require('sequelize');

// Get dashboard statistics
exports.getDashboardStats = async (req, res, next) => {
  try {
    // Get total users count
    const totalUsers = await User.count({
      where: { role: 'user' }
    });

    // Get total appointments count
    const totalAppointments = await Appointment.count();
    const totalBridalServices = await BridalService.count();

    // Get total orders count
    const totalOrders = await Order.count();

    // Get today's appointments
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];
    const todayAppointments = await Appointment.count({
      where: { appointmentDate: todayStr }
    });
    const todayBridalServices = await BridalService.count({
      where: { appointmentDate: todayStr }
    });

    // Get recent orders (last 30 days)
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    const recentOrders = await Order.count({
      where: {
        createdAt: {
          [Op.gte]: thirtyDaysAgo
        }
      }
    });

    // Get total revenue
    const totalRevenue = await Order.sum('totalAmount', {
      where: { paymentStatus: 'paid' }
    });

    res.status(200).json({
      success: true,
      data: {
        totalUsers,
        appointments: {
          total: totalAppointments + totalBridalServices,
          regular: totalAppointments,
          bridal: totalBridalServices,
          today: todayAppointments + todayBridalServices
        },
        orders: {
          total: totalOrders,
          recent: recentOrders
        },
        revenue: totalRevenue || 0
      }
    });
  } catch (error) {
    next(error);
  }
};

// Get all users
exports.getAllUsers = async (req, res, next) => {
  try {
    const users = await User.findAll({
      where: { role: 'user' },
      attributes: { exclude: ['password'] },
      order: [['createdAt', 'DESC']]
    });

    res.status(200).json({
      success: true,
      count: users.length,
      data: users
    });
  } catch (error) {
    next(error);
  }
};

// Get all appointments
exports.getAllAppointments = async (req, res, next) => {
  try {
    // Get regular appointments
    const appointments = await Appointment.findAll({
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'firstName', 'lastName', 'email']
        }
      ],
      order: [['appointmentDate', 'DESC']]
    });

    // Get bridal service appointments
    const bridalServices = await BridalService.findAll({
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'firstName', 'lastName', 'email']
        }
      ],
      order: [['appointmentDate', 'DESC']]
    });

    res.status(200).json({
      success: true,
      data: {
        appointments: {
          count: appointments.length,
          items: appointments
        },
        bridalServices: {
          count: bridalServices.length,
          items: bridalServices
        }
      }
    });
  } catch (error) {
    next(error);
  }
};

// Get all orders
exports.getAllOrders = async (req, res, next) => {
  try {
    const orders = await Order.findAll({
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'firstName', 'lastName', 'email']
        },
        {
          model: OrderItem,
          as: 'items',
          include: [
            {
              model: Product,
              as: 'product',
              attributes: ['id', 'name', 'price', 'imageUrl']
            }
          ]
        }
      ],
      order: [['createdAt', 'DESC']]
    });

    res.status(200).json({
      success: true,
      count: orders.length,
      data: orders
    });
  } catch (error) {
    next(error);
  }
};

// Manage products (get all products)
exports.getAllProducts = async (req, res, next) => {
  try {
    const products = await Product.findAll({
      order: [['createdAt', 'DESC']]
    });

    res.status(200).json({
      success: true,
      count: products.length,
      data: products
    });
  } catch (error) {
    next(error);
  }
};

// Add product
exports.addProduct = async (req, res, next) => {
  try {
    const {
      name,
      description,
      price,
      imageUrl,
      type,
      benefits,
      quantity,
      usage,
      ingredients,
      recommendedFor,
      extraInfo,
      stock
    } = req.body;

    // Create product
    const product = await Product.create({
      name,
      description,
      price,
      imageUrl,
      type,
      benefits,
      quantity,
      usage,
      ingredients,
      recommendedFor,
      extraInfo,
      stock: stock || 100
    });

    res.status(201).json({
      success: true,
      data: product
    });
  } catch (error) {
    next(error);
  }
};

// Update product
exports.updateProduct = async (req, res, next) => {
  try {
    const {
      name,
      description,
      price,
      imageUrl,
      type,
      benefits,
      quantity,
      usage,
      ingredients,
      recommendedFor,
      extraInfo,
      stock
    } = req.body;

    const product = await Product.findByPk(req.params.id);

    if (!product) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }

    // Update product fields
    if (name) product.name = name;
    if (description) product.description = description;
    if (price) product.price = price;
    if (imageUrl) product.imageUrl = imageUrl;
    if (type) product.type = type;
    if (benefits) product.benefits = benefits;
    if (quantity) product.quantity = quantity;
    if (usage) product.usage = usage;
    if (ingredients) product.ingredients = ingredients;
    if (recommendedFor) product.recommendedFor = recommendedFor;
    if (extraInfo) product.extraInfo = extraInfo;
    if (stock) product.stock = stock;

    await product.save();

    res.status(200).json({
      success: true,
      data: product
    });
  } catch (error) {
    next(error);
  }
};

// Delete product
exports.deleteProduct = async (req, res, next) => {
  try {
    const product = await Product.findByPk(req.params.id);

    if (!product) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }

    // Check if product is used in any order
    const orderItems = await OrderItem.findOne({
      where: { productId: req.params.id }
    });

    if (orderItems) {
      return res.status(400).json({
        success: false,
        message: 'Cannot delete product that is referenced in orders. Consider updating the stock to 0 instead.'
      });
    }

    await product.destroy();

    res.status(200).json({
      success: true,
      message: 'Product deleted successfully'
    });
  } catch (error) {
    console.error('Error in deleteProduct:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to delete product',
      error: error.message
    });
  }
};