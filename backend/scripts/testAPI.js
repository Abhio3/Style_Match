/**
 * API Testing Script
 * 
 * This script tests the backend API endpoints to make sure they're working correctly.
 * Run this script with: node scripts/testAPI.js
 */

require('dotenv').config();
const axios = require('axios');

// API base URL
const API_URL = process.env.API_URL || 'http://localhost:5000/api';

// Test account credentials
const testUser = {
  email: 'john@example.com',
  password: 'password123'
};

// Store tokens
let userToken = '';
let adminToken = '';

// Helper function for colored console output
const log = {
  success: (message) => console.log('\x1b[32m%s\x1b[0m', '✓ ' + message),
  error: (message) => console.log('\x1b[31m%s\x1b[0m', '✗ ' + message),
  info: (message) => console.log('\x1b[36m%s\x1b[0m', 'ℹ ' + message),
  warning: (message) => console.log('\x1b[33m%s\x1b[0m', '⚠ ' + message),
  section: (message) => console.log('\n\x1b[1m%s\x1b[0m', message)
};

// Test authentication endpoints
async function testAuth() {
  log.section('Testing Authentication Endpoints');
  
  try {
    // Test user login
    log.info('Testing user login...');
    const userLoginResponse = await axios.post(`${API_URL}/auth/login`, testUser);
    
    if (userLoginResponse.data.success) {
      userToken = userLoginResponse.data.token;
      log.success('User login successful');
    } else {
      log.error('User login failed');
    }
    
    // Test admin login
    log.info('Testing admin login...');
    const adminLoginResponse = await axios.post(`${API_URL}/auth/login`, {
      email: 'admin@stylematch.com',
      password: 'admin123'
    });
    
    if (adminLoginResponse.data.success) {
      adminToken = adminLoginResponse.data.token;
      log.success('Admin login successful');
    } else {
      log.error('Admin login failed');
    }
    
    // Test get current user
    if (userToken) {
      log.info('Testing get current user...');
      const userResponse = await axios.get(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${userToken}` }
      });
      
      if (userResponse.data.success) {
        log.success('Get current user successful');
      } else {
        log.error('Get current user failed');
      }
    }
    
    return true;
  } catch (error) {
    log.error(`Authentication tests failed: ${error.message}`);
    if (error.response) {
      console.error('Error response data:', error.response.data);
    }
    return false;
  }
}

// Test appointment endpoints
async function testAppointments() {
  log.section('Testing Appointment Endpoints');
  
  try {
    // Test create appointment
    log.info('Testing create appointment...');
    const appointmentData = {
      firstName: 'Test',
      lastName: 'User',
      gender: 'Male',
      mobile: '9876543299',
      email: 'test@example.com',
      service: 'Men Hair style',
      appointmentDate: '2025-06-30',
      appointmentTime: '3-5 PM'
    };
    
    const appointmentResponse = await axios.post(`${API_URL}/appointments/regular`, appointmentData);
    
    if (appointmentResponse.data.success) {
      log.success('Create appointment successful');
      const appointmentId = appointmentResponse.data.data.id;
      
      // Test get appointment (requires authentication)
      if (userToken) {
        log.info('Testing get appointment...');
        const getAppointmentResponse = await axios.get(`${API_URL}/appointments/regular/${appointmentId}`, {
          headers: { Authorization: `Bearer ${userToken}` }
        });
        
        if (getAppointmentResponse.data.success) {
          log.success('Get appointment successful');
        } else {
          log.error('Get appointment failed');
        }
      }
    } else {
      log.error('Create appointment failed');
    }
    
    // Test create bridal service
    log.info('Testing create bridal service...');
    const bridalData = {
      firstName: 'Bridal',
      lastName: 'Test',
      gender: 'Female',
      mobile: '9876543288',
      email: 'bridal@example.com',
      service: 'TRIAL MAKEUP SERVICE',
      appointmentDate: '2025-07-15',
      startTime: '10 AM',
      endTime: '2 PM',
      address: '123 Test St, Chennai'
    };
    
    const bridalResponse = await axios.post(`${API_URL}/appointments/bridal`, bridalData);
    
    if (bridalResponse.data.success) {
      log.success('Create bridal service successful');
    } else {
      log.error('Create bridal service failed');
    }
    
    return true;
  } catch (error) {
    log.error(`Appointment tests failed: ${error.message}`);
    if (error.response) {
      console.error('Error response data:', error.response.data);
    }
    return false;
  }
}

// Test order endpoints
async function testOrders() {
  log.section('Testing Order Endpoints');
  
  try {
    // Test create order
    log.info('Testing create order...');
    const orderData = {
      firstName: 'Order',
      lastName: 'Test',
      email: 'order@example.com',
      mobile: '9876543277',
      address: '456 Order St, Bangalore',
      paymentMethod: 'Cash on Delivery',
      items: [
        {
          productId: 1,
          quantity: 1
        },
        {
          productId: 2,
          quantity: 2
        }
      ]
    };
    
    const orderResponse = await axios.post(`${API_URL}/orders`, orderData);
    
    if (orderResponse.data.success) {
      log.success('Create order successful');
      const orderId = orderResponse.data.data.order.id;
      
      // Test get order (requires authentication)
      if (userToken) {
        log.info('Testing get order...');
        const getOrderResponse = await axios.get(`${API_URL}/orders/${orderId}`, {
          headers: { Authorization: `Bearer ${userToken}` }
        });
        
        if (getOrderResponse.data.success) {
          log.success('Get order successful');
        } else {
          log.error('Get order failed');
        }
      }
    } else {
      log.error('Create order failed');
    }
    
    return true;
  } catch (error) {
    log.error(`Order tests failed: ${error.message}`);
    if (error.response) {
      console.error('Error response data:', error.response.data);
    }
    return false;
  }
}

// Test admin endpoints
async function testAdmin() {
  log.section('Testing Admin Endpoints');
  
  if (!adminToken) {
    log.warning('Admin token not available. Skipping admin tests.');
    return false;
  }
  
  try {
    // Test dashboard stats
    log.info('Testing dashboard stats...');
    const statsResponse = await axios.get(`${API_URL}/admin/dashboard`, {
      headers: { Authorization: `Bearer ${adminToken}` }
    });
    
    if (statsResponse.data.success) {
      log.success('Dashboard stats successful');
    } else {
      log.error('Dashboard stats failed');
    }
    
    // Test get all users
    log.info('Testing get all users...');
    const usersResponse = await axios.get(`${API_URL}/admin/users`, {
      headers: { Authorization: `Bearer ${adminToken}` }
    });
    
    if (usersResponse.data.success) {
      log.success('Get all users successful');
    } else {
      log.error('Get all users failed');
    }
    
    // Test get all appointments
    log.info('Testing get all appointments...');
    const appointmentsResponse = await axios.get(`${API_URL}/admin/appointments`, {
      headers: { Authorization: `Bearer ${adminToken}` }
    });
    
    if (appointmentsResponse.data.success) {
      log.success('Get all appointments successful');
    } else {
      log.error('Get all appointments failed');
    }
    
    // Test get all orders
    log.info('Testing get all orders...');
    const ordersResponse = await axios.get(`${API_URL}/admin/orders`, {
      headers: { Authorization: `Bearer ${adminToken}` }
    });
    
    if (ordersResponse.data.success) {
      log.success('Get all orders successful');
    } else {
      log.error('Get all orders failed');
    }
    
    // Test get all products
    log.info('Testing get all products...');
    const productsResponse = await axios.get(`${API_URL}/admin/products`, {
      headers: { Authorization: `Bearer ${adminToken}` }
    });
    
    if (productsResponse.data.success) {
      log.success('Get all products successful');
    } else {
      log.error('Get all products failed');
    }
    
    return true;
  } catch (error) {
    log.error(`Admin tests failed: ${error.message}`);
    if (error.response) {
      console.error('Error response data:', error.response.data);
    }
    return false;
  }
}

// Run all tests
async function runTests() {
  log.section('Starting API Tests');
  log.info(`API URL: ${API_URL}`);
  
  try {
    // Auth tests
    const authSuccess = await testAuth();
    
    if (authSuccess) {
      // Run other tests if auth tests pass
      await testAppointments();
      await testOrders();
      await testAdmin();
      
      log.section('Tests Completed');
    } else {
      log.error('Auth tests failed. Skipping remaining tests.');
    }
  } catch (error) {
    log.error(`Error running tests: ${error.message}`);
  }
}

// Run the tests
runTests();