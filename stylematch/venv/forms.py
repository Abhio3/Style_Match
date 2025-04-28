from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = SelectField('Gender', choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')

class AppointmentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('', 'CHOOSE'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    service = SelectField('Service', choices=[
        ('', 'Select Service'),
        ('Men Hair style', 'Men Hair style'),
        ('Women Hair style', 'Women Hair style'),
        ('Beard Trim', 'Beard Trim'),
        ('Hair treatment', 'Hair treatment'),
        ('Skin treatment', 'Skin treatment')
    ], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = SelectField('Time', choices=[
        ('', 'CHOOSE'),
        ('8-10 AM', '8-10 AM'),
        ('10-12 AM', '10-12 AM'),
        ('1-3 PM', '1-3 PM'),
        ('3-5 PM', '3-5 PM'),
        ('5-7 PM', '5-7 PM'),
        ('7-9 PM', '7-9 PM'),
        ('9-11 PM', '9-11 PM')
    ], validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

class BridalAppointmentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('', 'CHOOSE'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    service = SelectField('Service', choices=[
        ('', 'Select Service'),
        ('TRIAL MAKEUP SERVICE', 'TRIAL MAKEUP SERVICE'),
        ('PRE-WEDDING MAKEUP SERVICE', 'PRE-WEDDING MAKEUP SERVICE'),
        ('MEHANDI SERVICE', 'MEHANDI SERVICE')
    ], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = StringField('Start Time', validators=[DataRequired()])
    start_ampm = SelectField('AM/PM', choices=[('AM', 'AM'), ('PM', 'PM')], validators=[DataRequired()])
    end_time = StringField('End Time', validators=[DataRequired()])
    end_ampm = SelectField('AM/PM', choices=[('AM', 'AM'), ('PM', 'PM')], validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

class OrderForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('', 'CHOOSE'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[
        ('', 'CHOOSE'),
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Online Payment', 'Online Payment')
    ], validators=[DataRequired()])
    submit = SubmitField('Proceed')