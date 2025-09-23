from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('restaurant', 'Restaurant/Hotel'), ('organization', 'Welfare Organization')], validators=[DataRequired()])
    name = StringField('Restaurant/Organization Name', validators=[DataRequired()])
    address = StringField('Address')
    registration_number = StringField('Govt. Registration Number (if Organization)', validators=[Optional()])
    submit = SubmitField('Register')

    def validate_registration_number(self, registration_number):
        if self.role.data == 'organization' and not registration_number.data:
            raise ValidationError("Organizations must provide a valid government registration number.")

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Food Post Form
class FoodPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description (optional)')
    quantity = StringField('Quantity', validators=[DataRequired()])
    pickup_time = StringField('Pickup Time', validators=[DataRequired()])
    submit = SubmitField('Post Food')
