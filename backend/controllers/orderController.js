const { Order, OrderItem } = require('../models/Order');
const Product = require('../models/Product');
const { sequelize } = require('../config/database');

// Create a new order
exports.createOrder = async (req, res, next) => {
  // Start a transaction to ensure all database operations succeed or fail together
  const transaction = await sequelize.transaction();

  try {
    const {
      firstName,
      lastName,
      email,
      mobile,
      address,
      paymentMethod,
      items
    } = req.body;

    // Validate input
    if (!items || !Array.isArray(items) || items.length === 0) {
      await transaction.rollback();
      return res.status(400).json({
        success: false,
        message: 'Order must contain at least one item'
      });
    }

    // Calculate total amount
    let totalAmount = 0;
    const orderItems = [];

    // Get product details and validate items
    for (const item of items) {
      const product = await Product.findByPk(item.productId);

      if (!product) {
        await transaction.rollback();
        return res.status(404).json({
          success: false,
          message: `Product with ID ${item.productId} not found`
        });
      }

      // Check stock
      if (product.stock < item.quantity) {
        await transaction.rollback();
        return res.status(400).json({
          success: false,
          message: `Not enough stock for product ${product.name}`
        });
      }

      totalAmount += product.price * item.quantity;

      orderItems.push({
        productId: product.id,
        quantity: item.quantity,
        price: product.price
      });

      // Update product stock
      product.stock -= item.quantity;
      await product.save({ transaction });
    }

    // Create order
    const order = await Order.create({
      userId: req.user ? req.user.id : null,
      firstName,
      lastName,
      email,
      mobile,
      address,
      totalAmount,
      paymentMethod,
      paymentStatus: paymentMethod === 'Cash on Delivery' ? 'pending' : 'pending'
    }, { transaction });

    // Create order items
    for (const item of orderItems) {
      await OrderItem.create({
        orderId: order.id,
        productId: item.productId,
        quantity: item.quantity,
        price: item.price
      }, { transaction });
    }

    // If payment method is online payment, we would typically redirect to a payment gateway
    // For demonstration purposes, we'll just simulate payment success

    // Commit transaction
    await transaction.commit();

    res.status(201).json({
      success: true,
      data: {
        order,
        paymentUrl: paymentMethod === 'Online Payment' ? 
          `https://example.com/payment/${order.id}` : null
      }
    });
  } catch (error) {
    // Rollback transaction in case of error
    await transaction.rollback();
    next(error);
  }
};

// Get user orders
exports.getUserOrders = async (req, res, next) => {
  try {
    const orders = await Order.findAll({
      where: { userId: req.user.id },
      include: [
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
      data: orders
    });
  } catch (error) {
    next(error);
  }
};

// Get order by ID
exports.getOrder = async (req, res, next) => {
  try {
    const order = await Order.findByPk(req.params.id, {
      include: [
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
      ]
    });

    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Order not found'
      });
    }

    // Check if user is authorized to view this order
    if (req.user.role !== 'admin' && order.userId !== req.user.id) {
      return res.status(403).json({
        success: false,
        message: 'Not authorized to access this order'
      });
    }

    res.status(200).json({
      success: true,
      data: order
    });
  } catch (error) {
    next(error);
  }
};

// Update order status
exports.updateOrderStatus = async (req, res, next) => {
  try {
    const { orderStatus, paymentStatus } = req.body;

    // Validate status values
    if (orderStatus && !['processing', 'shipped', 'delivered', 'cancelled'].includes(orderStatus)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid order status value'
      });
    }

    if (paymentStatus && !['pending', 'paid', 'failed'].includes(paymentStatus)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid payment status value'
      });
    }

    const order = await Order.findByPk(req.params.id);

    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Order not found'
      });
    }

    // Only admin can update order status
    if (req.user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: 'Not authorized to update this order'
      });
    }

    // Update order
    if (orderStatus) order.orderStatus = orderStatus;
    if (paymentStatus) order.paymentStatus = paymentStatus;
    
    await order.save();

    res.status(200).json({
      success: true,
      data: order
    });
  } catch (error) {
    next(error);
  }
};

// Handle payment callback
exports.handlePaymentCallback = async (req, res, next) => {
  // This would typically be called by the payment gateway after payment processing
  try {
    const { orderId, status, transactionId } = req.body;

    const order = await Order.findByPk(orderId);

    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Order not found'
      });
    }

    // Update payment status based on payment gateway response
    order.paymentStatus = status === 'success' ? 'paid' : 'failed';
    
    // If payment failed, we could handle restoring inventory here
    
    await order.save();

    res.status(200).json({
      success: true,
      data: order
    });
  } catch (error) {
    next(error);
  }
};