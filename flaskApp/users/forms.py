from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskApp.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')




class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')




class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')




class AdminRegistrationForm(FlaskForm):
    username = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    designation = StringField(label='Designation', validators=[DataRequired(),])
    dept = StringField(label='Department', validators=[DataRequired(),])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_designation(self, designation):
        d = ['HOD', 'Professor', 'Asst.Professor','Asst. Professor', 'Principal', 'Alumni', 'Others']
        if designation.data not in d:
            raise ValidationError("Please choose from 'HOD', 'Professor', 'Asst. Professor', 'Principal', 'Alumni', 'Others' only")            

    def validate_dept(self, dept):
        depts = ['CSE', 'ECE', 'EEE', 'ME', 'CE', 'IT', 'Others']
        if dept.data not in depts:
            raise ValidationError("Please choose from 'CSE', 'ECE', 'EEE', 'ME', 'CE', 'IT', 'Others' only")            




class AdminUpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    designation = StringField(label='Designation', validators=[DataRequired(),])
    dept = StringField(label='Department', validators=[DataRequired(),])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.is_admin == True:
            if username.data != current_user.username:
                user = User.query.filter_by(username=username.data).first()
                if user:
                    raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if current_user.is_admin == True:
            if email.data != current_user.email:
                user = User.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError('That email is taken. Please choose a different one.')

    def validate_designation(self, designation):
        if current_user.is_admin == True:
            if designation.data != current_user.designation:
                user = User.query.filter_by(designation=designation.data).first()
                d = ['HOD', 'Professor', 'Asst.Professor','Asst. Professor', 'Principal', 'Alumni', 'Others']
                if designation.data not in d:
                    raise ValidationError("Please choose from 'HOD', 'Professor', 'Asst. Professor', 'Principal', 'Alumni', 'Others' only")

    def validate_dept(self, dept):
        if current_user.is_admin == True:
            if dept.data != current_user.dept:
                user = User.query.filter_by(dept=dept.data).first()
                d = ['CSE', 'ECE', 'EEE', 'ME', 'CE', 'IT', 'Others']
                if dept.data not in d:
                    raise ValidationError("Please choose from 'CSE', 'ECE', 'EEE', 'ME', 'CE', 'IT', 'Others' only")