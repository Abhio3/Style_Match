const Appointment = require('../models/Appointment');
const BridalService = require('../models/BridalService');
const User = require('../models/User');

// Create regular appointment
exports.createAppointment = async (req, res, next) => {
  try {
    const {
      firstName,
      lastName,
      gender,
      mobile,
      email,
      service,
      appointmentDate,
      appointmentTime
    } = req.body;

    // Check if appointmentDate is in valid format (YYYY-MM-DD)
    if (!/^\d{4}-\d{2}-\d{2}$/.test(appointmentDate)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid date format. Please use YYYY-MM-DD format'
      });
    }

    // Create appointment
    const appointment = await Appointment.create({
      firstName,
      lastName,
      gender,
      mobile,
      email,
      service,
      appointmentDate,
      appointmentTime,
      userId: req.user ? req.user.id : null // If user is logged in
    });

    res.status(201).json({
      success: true,
      data: appointment
    });
  } catch (error) {
    next(error);
  }
};

// Create bridal service appointment
exports.createBridalAppointment = async (req, res, next) => {
  try {
    const {
      firstName,
      lastName,
      gender,
      mobile,
      email,
      service,
      appointmentDate,
      startTime,
      endTime,
      address
    } = req.body;

    // Check if appointmentDate is in valid format (YYYY-MM-DD)
    if (!/^\d{4}-\d{2}-\d{2}$/.test(appointmentDate)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid date format. Please use YYYY-MM-DD format'
      });
    }

    // Create bridal service appointment
    const bridalService = await BridalService.create({
      firstName,
      lastName,
      gender,
      mobile,
      email,
      service,
      appointmentDate,
      startTime,
      endTime,
      address,
      userId: req.user ? req.user.id : null // If user is logged in
    });

    res.status(201).json({
      success: true,
      data: bridalService
    });
  } catch (error) {
    next(error);
  }
};

// Get all appointments for a user
exports.getUserAppointments = async (req, res, next) => {
  try {
    // Find regular appointments
    const appointments = await Appointment.findAll({
      where: { userId: req.user.id },
      order: [['appointmentDate', 'DESC']]
    });

    // Find bridal service appointments
    const bridalServices = await BridalService.findAll({
      where: { userId: req.user.id },
      order: [['appointmentDate', 'DESC']]
    });

    res.status(200).json({
      success: true,
      data: {
        appointments,
        bridalServices
      }
    });
  } catch (error) {
    next(error);
  }
};

// Get appointment by ID
exports.getAppointment = async (req, res, next) => {
  try {
    const appointment = await Appointment.findByPk(req.params.id);

    if (!appointment) {
      return res.status(404).json({
        success: false,
        message: 'Appointment not found'
      });
    }

    // Check if user is authorized to view this appointment
    if (req.user.role !== 'admin' && appointment.userId !== req.user.id) {
      return res.status(403).json({
        success: false,
        message: 'Not authorized to access this appointment'
      });
    }

    res.status(200).json({
      success: true,
      data: appointment
    });
  } catch (error) {
    next(error);
  }
};

// Get bridal service appointment by ID
exports.getBridalAppointment = async (req, res, next) => {
  try {
    const bridalService = await BridalService.findByPk(req.params.id);

    if (!bridalService) {
      return res.status(404).json({
        success: false,
        message: 'Bridal service appointment not found'
      });
    }

    // Check if user is authorized to view this appointment
    if (req.user.role !== 'admin' && bridalService.userId !== req.user.id) {
      return res.status(403).json({
        success: false,
        message: 'Not authorized to access this appointment'
      });
    }

    res.status(200).json({
      success: true,
      data: bridalService
    });
  } catch (error) {
    next(error);
  }
};

// Update appointment status
exports.updateAppointmentStatus = async (req, res, next) => {
  try {
    const { status } = req.body;

    // Check if status is valid
    if (!['pending', 'confirmed', 'canceled', 'completed'].includes(status)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid status value'
      });
    }

    const appointment = await Appointment.findByPk(req.params.id);

    if (!appointment) {
      return res.status(404).json({
        success: false,
        message: 'Appointment not found'
      });
    }

    // Only admin can update appointment status (or the user can cancel their own appointment)
    if (req.user.role !== 'admin' && 
        (appointment.userId !== req.user.id || status !== 'canceled')) {
      return res.status(403).json({
        success: false,
        message: 'Not authorized to update this appointment'
      });
    }

    // Update appointment
    appointment.status = status;
    await appointment.save();

    res.status(200).json({
      success: true,
      data: appointment
    });
  } catch (error) {
    next(error);
  }
};

// Update bridal service appointment status
exports.updateBridalAppointmentStatus = async (req, res, next) => {
  try {
    const { status } = req.body;

    // Check if status is valid
    if (!['pending', 'confirmed', 'canceled', 'completed'].includes(status)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid status value'
      });
    }

    const bridalService = await BridalService.findByPk(req.params.id);

    if (!bridalService) {
      return res.status(404).json({
        success: false,
        message: 'Bridal service appointment not found'
      });
    }

    // Only admin can update appointment status (or the user can cancel their own appointment)
    if (req.user.role !== 'admin' && 
        (bridalService.userId !== req.user.id || status !== 'canceled')) {
      return res.status(403).json({
        success: false,
        message: 'Not authorized to update this appointment'
      });
    }

    // Update appointment
    bridalService.status = status;
    await bridalService.save();

    res.status(200).json({
      success: true,
      data: bridalService
    });
  } catch (error) {
    next(error);
  }
};