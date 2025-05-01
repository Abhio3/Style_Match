require('dotenv').config();

module.exports = {
  // JWT configuration
  jwt: {
    secret: process.env.JWT_SECRET || 'stylematch-secret-key',
    expiresIn: process.env.JWT_EXPIRES_IN || '1d'
  },
  
  // Application configuration
  app: {
    port: process.env.PORT || 5000,
    environment: process.env.NODE_ENV || 'development'
  },
  
  // User roles
  roles: {
    USER: 'user',
    ADMIN: 'admin'
  }
};