// StyleMatch API Integration
const API_URL = 'http://localhost:5000/api';

// Authentication functions
const auth = {
  // Register a new user
  register: async (userData) => {
    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });
      return await response.json();
    } catch (error) {
      console.error('Error registering user:', error);
      return { success: false, message: 'Network error occurred' };
    }
  },

  // Login user
  login: async (email, password) => {
    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
      const data = await response.json();
      
      if (data.success && data.token) {
        // Store token in localStorage
        localStorage.setItem('styleMatchToken', data.token);
        localStorage.setItem('styleMatchUser', JSON.stringify(data.user));
      }
      
      return data;
    } catch (error) {
      console.error('Error logging in:', error);
      return { success: false, message: 'Network error occurred' };
    }
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('styleMatchToken');
    localStorage.removeItem('styleMatchUser');
    window.location.href = 'index.html';
  },

  // Get current user
  getCurrentUser: () => {
    const user = localStorage.getItem('styleMatchUser');
    return user ? JSON.parse(user) : null;
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return localStorage.getItem('styleMatchToken') !== null;
  },

  // Check if user is admin
  isAdmin: () => {
    const user = auth.getCurrentUser();
    return user && user.role === 'admin';
  },

  // Get authentication token
  getToken: () => {
    return localStorage.getItem('styleMatchToken');
  },

  // Reset password request
  forgotPassword: async (email) => {
    try {
      const response = await fetch(`${API_URL}/auth/forgotpassword`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })
      });
      return await response.json();
    } catch (error) {
      console.error('Error requesting password reset:', error);
      return { success: false, message: 'Network error occurred' };
    }
  }
};

// Appointment functions
const appointments = {
  // Book a regular appointment
  bookRegular: async (appointmentData) => {
    try {
      const response = await fetch(`${API_URL}/appointments/regular`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(auth.isAuthenticated() && { 'Authorization': `Bearer ${auth.getToken()}` })
        },
        body: JSON.stringify(appointmentData)
      });
      
      const data = await response.json();
      
      // If appointment is successful and user is logged in, add to orders list in localStorage
      if (data.success && auth.isAuthenticated()) {
        const orders = JSON.parse(localStorage.getItem('styleMatchOrders') || '[]');
        const newAppointment = {
          type: 'Appointment',
          name: `${appointmentData.firstName} ${appointmentData.lastName}`,
          mobile: appointmentData.mobile,
          service: appointmentData.service,
          date: appointmentData.appointmentDate,
          time: appointmentData.appointmentTime
        };
        orders.push(newAppointment);
        localStorage.setItem('styleMatchOrders', JSON.stringify(orders));
      }
      
      return data;
    } catch (error) {
      console.error('Error booking appointment:', error);
      return { success: false, message: 'Network error occurred' };
    }
  },

  // Book a bridal service appointment
  bookBridal: async (appointmentData) => {
    try {
      const response = await fetch(`${API_URL}/appointments/bridal`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(auth.isAuthenticated() && { 'Authorization': `Bearer ${auth.getToken()}` })
        },
        body: JSON.stringify(appointmentData)
      });
      
      const data = await response.json();
      
      // If appointment is successful and user is logged in, add to orders list in localStorage
      if (data.success && auth.isAuthenticated()) {
        const orders = JSON.parse(localStorage.getItem('styleMatchOrders') || '[]');
        const newAppointment = {
          type: 'Bridal Service',
          name: `${appointmentData.firstName} ${appointmentData.lastName}`,
          mobile: appointmentData.mobile,
          service: appointmentData.service,
          date: appointmentData.appointmentDate,
          time: `${appointmentData.startTime} to ${appointmentData.endTime}`,
          address: appointmentData.address
        };
        orders.push(newAppointment);
        localStorage.setItem('styleMatchOrders', JSON.stringify(orders));
      }
      
      return data;
    } catch (error) {
      console.error('Error booking bridal service:', error);
      return { success: false, message: 'Network error occurred' };
    }
  },

  // Get user appointments
  getUserAppointments: async () => {
    if (!auth.isAuthenticated()) {
      return { success: false, message: 'User not authenticated' };
    }

    try {
      const response = await fetch(`${API_URL}/appointments/user`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${auth.getToken()}`
        }
      });
      return await response.json();
    } catch (error) {
      console.error('Error fetching appointments:', error);
      return { success: false, message: 'Network error occurred' };
    }
  }
};

// Order functions
const orders = {
  // Create a new order
  createOrder: async (orderData) => {
    try {
      const response = await fetch(`${API_URL}/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(auth.isAuthenticated() && { 'Authorization': `Bearer ${auth.getToken()}` })
        },
        body: JSON.stringify(orderData)
      });
      
      const data = await response.json();
      
      // If order is successful, add to orders list in localStorage
      if (data.success) {
        const orders = JSON.parse(localStorage.getItem('styleMatchOrders') || '[]');
        const newOrder = {
          type: 'Product Order',
          name: `${orderData.firstName} ${orderData.lastName}`,
          mobile: orderData.mobile,
          paymentMethod: orderData.paymentMethod,
          items: JSON.parse(localStorage.getItem('cartItems') || '[]'),
          totalAmount: orderData.items.reduce((total, item) => total + (item.price * item.quantity), 0)
        };
        orders.push(newOrder);
        localStorage.setItem('styleMatchOrders', JSON.stringify(orders));
        
        // Clear cart after successful order
        localStorage.removeItem('cartItems');
      }
      
      return data;
    } catch (error) {
      console.error('Error creating order:', error);
      return { success: false, message: 'Network error occurred' };
    }
  },

  // Get user orders
  getUserOrders: async () => {
    if (!auth.isAuthenticated()) {
      return { success: false, message: 'User not authenticated' };
    }

    try {
      const response = await fetch(`${API_URL}/orders/user`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${auth.getToken()}`
        }
      });
      return await response.json();
    } catch (error) {
      console.error('Error fetching orders:', error);
      return { success: false, message: 'Network error occurred' };
    }
  }
};

// Admin functions
const admin = {
  // Get dashboard statistics
  getDashboardStats: async () => {
    if (!auth.isAdmin()) {
      return { success: false, message: 'Unauthorized access' };
    }

    try {
      const response = await fetch(`${API_URL}/admin/dashboard`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${auth.getToken()}`
        }
      });
      return await response.json();
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      return { success: false, message: 'Network error occurred' };
    }
  },

  // Get all users
  getAllUsers: async () => {
    if (!auth.isAdmin()) {
      return { success: false, message: 'Unauthorized access' };
    }

    try {
      const response = await fetch(`${API_URL}/admin/users`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${auth.getToken()}`
        }
      });
      return await response.json();
    } catch (error) {
      console.error('Error fetching users:', error);
      return { success: false, message: 'Network error occurred' };
    }
  },

  // Get all appointments
  getAllAppointments: async () => {
    if (!auth.isAdmin()) {
      return { success: false, message: 'Unauthorized access' };
    }

    try {
      const response = await fetch(`${API_URL}/admin/appointments`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${auth.getToken()}`
        }
      });
      return await response.json();
    } catch (error) {
      console.error('Error fetching appointments:', error);
      return { success: false, message: 'Network error occurred' };
    }
  },

  // Get all orders
  getAllOrders: async () => {
    if (!auth.isAdmin()) {
      return { success: false, message: 'Unauthorized access' };
    }

    try {
      const response = await fetch(`${API_URL}/admin/orders`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${auth.getToken()}`
        }
      });
      return await response.json();
    } catch (error) {
      console.error('Error fetching orders:', error);
      return { success: false, message: 'Network error occurred' };
    }
  },

  // Manage products
  getAllProducts: async () => {
    if (!auth.isAdmin()) {
      return { success: false, message: 'Unauthorized access' };
    }

    try {
      const response = await fetch(`${API_URL}/admin/products`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${auth.getToken()}`
        }
      });
      return await response.json();
    } catch (error) {
      console.error('Error fetching products:', error);
      return { success: false, message: 'Network error occurred' };
    }
  }
};

// Export API functions
window.styleMatchAPI = {
  auth,
  appointments,
  orders,
  admin
};