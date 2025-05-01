# StyleMatch Salon Backend

This is the backend implementation for the StyleMatch Salon website. It provides a complete API for user authentication, appointment bookings, order processing, and an admin dashboard.

## Features

- **User Authentication**: Register, login, and profile management
- **Role-Based Authorization**: User and admin roles with appropriate permissions
- **Appointment Booking**: Regular and bridal service appointment management
- **Order Processing**: Product orders with payment integration
- **Admin Dashboard**: Comprehensive management of users, appointments, orders, and products

## Technologies Used

- **Backend**: Node.js, Express.js
- **Database**: MySQL with Sequelize ORM
- **Authentication**: JWT (JSON Web Tokens)
- **API**: RESTful API design

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- MySQL Server

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stylematch-backend.git
   cd backend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the root directory based on the `.env.template` file:
   ```
   PORT=5000
   NODE_ENV=development
   DB_HOST=localhost
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_NAME=stylematch_db
   JWT_SECRET=your_jwt_secret_key
   JWT_EXPIRES_IN=1d
   ```

4. Set up the database:
   ```bash
   # Create database and tables
   node utils/dbInit.js
   ```

5. Start the server:
   ```bash
   npm start
   ```

   For development with auto-reload:
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/forgotpassword` - Request password reset
- `POST /api/auth/resetpassword` - Reset password

### Appointments

- `POST /api/appointments/regular` - Book a regular appointment
- `POST /api/appointments/bridal` - Book a bridal service appointment
- `GET /api/appointments/user` - Get user appointments
- `GET /api/appointments/regular/:id` - Get appointment by ID
- `GET /api/appointments/bridal/:id` - Get bridal service by ID
- `PUT /api/appointments/regular/:id/status` - Update appointment status
- `PUT /api/appointments/bridal/:id/status` - Update bridal service status

### Orders

- `POST /api/orders` - Create a new order
- `GET /api/orders/user` - Get user orders
- `GET /api/orders/:id` - Get order by ID
- `PUT /api/orders/:id/status` - Update order status
- `POST /api/orders/payment/callback` - Handle payment callback

### Admin

- `GET /api/admin/dashboard` - Get dashboard statistics
- `GET /api/admin/users` - Get all users
- `GET /api/admin/appointments` - Get all appointments
- `GET /api/admin/orders` - Get all orders
- `GET /api/admin/products` - Get all products
- `POST /api/admin/products` - Add a new product
- `PUT /api/admin/products/:id` - Update a product
- `DELETE /api/admin/products/:id` - Delete a product

## Frontend Integration

To integrate this backend with the frontend:

1. Include the `public/js/api.js` script in your HTML files:
   ```html
   <script src="js/api.js"></script>
   ```

2. Use the provided API functions to interact with the backend:
   ```javascript
   // Authentication
   await styleMatchAPI.auth.register(userData);
   await styleMatchAPI.auth.login(email, password);
   
   // Appointments
   await styleMatchAPI.appointments.bookRegular(appointmentData);
   await styleMatchAPI.appointments.bookBridal(bridalData);
   
   // Orders
   await styleMatchAPI.orders.createOrder(orderData);
   ```

## Admin Dashboard

Access the admin dashboard at `/admin.html`. You can:

- View overall statistics
- Manage users
- Handle appointments and bridal services
- Process orders
- Manage products

## License

This project is licensed under the MIT License - see the LICENSE file for details.
