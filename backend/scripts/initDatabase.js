/**
 * Database Initialization Script
 * 
 * This script creates all necessary tables and populates them with sample data.
 * Run this script with: node scripts/initDatabase.js
 */

require('dotenv').config();
const bcrypt = require('bcryptjs');
const { sequelize } = require('../config/database');
const User = require('../models/User');
const { Order, OrderItem } = require('../models/Order');
const Product = require('../models/Product');
const Appointment = require('../models/Appointment');
const BridalService = require('../models/BridalService');

// Sample data for initial database setup
const users = [
  {
    firstName: 'Admin',
    lastName: 'User',
    email: 'admin@stylematch.com',
    password: 'admin123',
    gender: 'Male',
    mobile: '9876543210',
    role: 'admin'
  },
  {
    firstName: 'John',
    lastName: 'Doe',
    email: 'john@example.com',
    password: 'password123',
    gender: 'Male',
    mobile: '9876543211',
    role: 'user'
  },
  {
    firstName: 'Jane',
    lastName: 'Smith',
    email: 'jane@example.com',
    password: 'password123',
    gender: 'Female',
    mobile: '9876543212',
    role: 'user'
  }
];

const products = [
  {
    name: 'Face Cream',
    description: 'Natural Herbal Moisturizing Cream',
    price: 1500,
    imageUrl: 'images/facecream2.png',
    type: 'Face Cream (Type)',
    benefits: 'Deeply hydrates skin, reduces pigmentation, and improves skin elasticity.',
    quantity: '100ml',
    usage: 'Apply gently on cleansed face twice a day for best results.',
    ingredients: 'Aloe Vera, Turmeric, Licorice Extract, Vitamin E',
    recommendedFor: 'All Skin Types',
    extraInfo: 'Free from Sulphates, Parabens, and Artificial Fragrances. Dermatologically Tested.',
    stock: 50
  },
  {
    name: 'Hair Mask',
    description: 'Proprietary Ayurvedic Product',
    price: 750,
    imageUrl: 'images/HairMask.png',
    type: 'Hair Treatment',
    benefits: 'Strengthens hair, reduces hair fall',
    quantity: '200ml',
    usage: 'Apply on clean, damp hair from root to tips, avoiding the scalp. Leave for 3 mins, then rinse.',
    ingredients: 'Bringharaj, Neem, Amla, Rosemary oil, Basil oil, Orange oil, Cedarwood oil',
    recommendedFor: 'Men & Women',
    extraInfo: 'Non-greasy feel post wash',
    stock: 75
  },
  {
    name: 'Hair Shampoo',
    description: 'Ayurvedic Shampoo (Medicine)',
    price: 1200,
    imageUrl: 'images/shampoo_image.png',
    type: 'Hair Shampoo (Type)',
    benefits: 'Reduces Hair Fall in 4 washes – due to breakage.',
    quantity: '200ml',
    usage: 'Apply 3 times a week Stylematch Shampoo,one day after one day, for best results.',
    ingredients: 'Bringha (Bringharaj) plant extract, Shikakai, Amla, Rosemary oil',
    recommendedFor: 'Men & Women',
    extraInfo: '100% free from Parabens, Synthetic Dyes & Synthetic Perfumes.',
    stock: 80
  },
  {
    name: 'Hair Oil',
    description: '100% Ayurvedic Hair Oil (Medicine)',
    price: 1400,
    imageUrl: 'images/hairoil_image.png',
    type: 'Hair Oil (Type)',
    benefits: 'Clinically proven to Grow new hair and Reduce hair fall.',
    quantity: '250ml',
    usage: 'For best results use 3 times a week for 4 months. Post applying the oil leave it for 3–4 hours and then rinse it off using Indulekha Bringha Shampoo.',
    ingredients: 'Bringhraj, Svetakutaja, Amla, Virgin Coconut Oil',
    recommendedFor: 'Men & Women',
    extraInfo: '100% free from Parabens, Sulphates (Sulfates), Silicones, Synthetic Dyes & Synthetic Perfumes.',
    stock: 80
  }
];

const appointments = [
  {
    firstName: 'John',
    lastName: 'Doe',
    gender: 'Male',
    mobile: '9876543211',
    email: 'john@example.com',
    service: 'Men Hair style',
    appointmentDate: '2025-06-01',
    appointmentTime: '10-12 AM',
    status: 'confirmed',
    userId: 2
  },
  {
    firstName: 'Jane',
    lastName: 'Smith',
    gender: 'Female',
    mobile: '9876543212',
    email: 'jane@example.com',
    service: 'Women Hair style',
    appointmentDate: '2025-06-02',
    appointmentTime: '1-3 PM',
    status: 'pending',
    userId: 3
  }
];

const bridalServices = [
  {
    firstName: 'Jane',
    lastName: 'Smith',
    gender: 'Female',
    mobile: '9876543212',
    email: 'jane@example.com',
    service: 'TRIAL MAKEUP SERVICE',
    appointmentDate: '2025-06-15',
    startTime: '10 AM',
    endTime: '2 PM',
    address: '123 Main St, New Delhi',
    status: 'confirmed',
    userId: 3
  }
];

const orders = [
  {
    userId: 2,
    firstName: 'John',
    lastName: 'Doe',
    email: 'john@example.com',
    mobile: '9876543211',
    address: '123 Main St, New Delhi',
    totalAmount: 2250,
    paymentMethod: 'Online Payment',
    paymentStatus: 'paid',
    orderStatus: 'delivered'
  },
  {
    userId: 3,
    firstName: 'Jane',
    lastName: 'Smith',
    email: 'jane@example.com',
    mobile: '9876543212',
    address: '456 Park Ave, Mumbai',
    totalAmount: 1400,
    paymentMethod: 'Cash on Delivery',
    paymentStatus: 'pending',
    orderStatus: 'processing'
  }
];

const orderItems = [
  {
    orderId: 1,
    productId: 1,
    quantity: 1,
    price: 1500
  },
  {
    orderId: 1,
    productId: 2,
    quantity: 1,
    price: 750
  },
  {
    orderId: 2,
    productId: 4,
    quantity: 1,
    price: 1400
  }
];

// Initialize database
async function initializeDatabase() {
  try {
    console.log('Syncing database...');
    
    // Force true - Drop existing tables and re-create
    await sequelize.sync({ force: true });
    console.log('Database synchronized!');
    
    // Create admin and sample users
    console.log('Creating users...');
    const hashedUsers = [];
    for (const user of users) {
      const salt = await bcrypt.genSalt(10);
      const hashedPassword = await bcrypt.hash(user.password, salt);
      
      hashedUsers.push({
        ...user,
        password: hashedPassword
      });
    }
    
    const createdUsers = await User.bulkCreate(hashedUsers);
    console.log(`Created ${createdUsers.length} users successfully!`);
    
    // Create products
    console.log('Creating products...');
    const createdProducts = await Product.bulkCreate(products);
    console.log(`Created ${createdProducts.length} products successfully!`);
    
    // Create appointments
    console.log('Creating appointments...');
    const createdAppointments = await Appointment.bulkCreate(appointments);
    console.log(`Created ${createdAppointments.length} appointments successfully!`);
    
    // Create bridal services
    console.log('Creating bridal services...');
    const createdBridalServices = await BridalService.bulkCreate(bridalServices);
    console.log(`Created ${createdBridalServices.length} bridal services successfully!`);
    
    // Create orders
    console.log('Creating orders...');
    const createdOrders = await Order.bulkCreate(orders);
    console.log(`Created ${createdOrders.length} orders successfully!`);
    
    // Create order items
    console.log('Creating order items...');
    const createdOrderItems = await OrderItem.bulkCreate(orderItems);
    console.log(`Created ${createdOrderItems.length} order items successfully!`);
    
    console.log('Database initialization completed successfully!');
    process.exit(0);
  } catch (error) {
    console.error('Error initializing database:', error);
    process.exit(1);
  }
}

// Run the initialization
initializeDatabase();