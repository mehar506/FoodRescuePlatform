from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )

    role = SelectField(
        'Role',
        choices=[('restaurant', 'Restaurant/Hotel'),
                 ('organization', 'Welfare Organization')],
        validators=[DataRequired()]
    )
    name = StringField('Restaurant/Organization Name', validators=[DataRequired()])
    address = StringField('Address')

    # Only for organizations
    registration_number = StringField(
        'Govt. Registration Number (if Organization)',
        validators=[Optional()]
    )

    submit = SubmitField('Register')

    # Custom validation: enforce registration number if role is organization
    def validate_registration_number(self, registration_number):
        if self.role.data == 'organization' and not registration_number.data:
            raise ValidationError("Organizations must provide a valid government registration number.")
