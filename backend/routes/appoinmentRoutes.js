const express = require('express');
const {
  createAppointment,
  createBridalAppointment,
  getUserAppointments,
  getAppointment,
  getBridalAppointment,
  updateAppointmentStatus,
  updateBridalAppointmentStatus
} = require('../controllers/appointmentController');
const { protect } = require('../middlewares/auth');

const router = express.Router();

// Public routes (anyone can book an appointment without authentication)
router.post('/regular', createAppointment);
router.post('/bridal', createBridalAppointment);

// Protected routes
router.get('/user', protect, getUserAppointments);
router.get('/regular/:id', protect, getAppointment);
router.get('/bridal/:id', protect, getBridalAppointment);
router.put('/regular/:id/status', protect, updateAppointmentStatus);
router.put('/bridal/:id/status', protect, updateBridalAppointmentStatus);

module.exports = router;