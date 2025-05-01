const { sequelize } = require('../config/database');
const User = require('../models/User');
const Product = require('../models/Product');
const config = require('../config/config');

// Initialize database with some sample data
const initializeDb = async () => {
  try {
    // Sync database (create tables)
    await sequelize.sync({ force: true });
    console.log('Database synced successfully');

    // Create admin user
    await User.create({
      firstName: 'Admin',
      lastName: 'User',
      email: 'admin@stylematch.com',
      password: 'admin123',
      gender: 'Male',
      mobile: '9876543210',
      role: config.roles.ADMIN
    });
    console.log('Admin user created');

    // Create sample products
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
        stock: 60
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

    for (const product of products) {
      await Product.create(product);
    }
    console.log('Sample products created');

    console.log('Database initialization completed successfully');
  } catch (error) {
    console.error('Error initializing database:', error);
  }
};

// Execute if script is run directly
if (require.main === module) {
  initializeDb();
}

module.exports = initializeDb;