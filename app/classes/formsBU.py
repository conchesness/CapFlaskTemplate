# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask.app import Flask
from flask import flash
from flask_wtf import FlaskForm
from mongoengine.fields import EmailField
import mongoengine.errors
from wtforms.validators import URL, NumberRange, Email, Optional, InputRequired, ValidationError, DataRequired, EqualTo
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, HiddenField, IntegerField, SelectField, FileField, BooleanField
from app.classes.data import User

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    role = SelectField('Role',choices=[("Teacher","Teacher"),("Student","Student")])
    school = SelectField('School',choices=[("Oakland Technical High School","Oakland Technical High School")])
    image = FileField("Image") 
    role = SelectField('role',choices=[("Teacher","Teacher"),("Student", "Student")])
    submit = SubmitField('Post')

class PostForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Post', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class CoursesForm(FlaskForm): 
    course_number = StringField('Course Number', validators=[DataRequired()])
    course_title = StringField('Course Title', validators=[DataRequired()])
    course_name = StringField('Course Name', validators=[DataRequired()])
    course_ag_requirement = SelectField('Courses A-G Requirement',choices=[("",""),("A-History","A-History"),("B-English", "B-English"), ("C-Mathematics","C-Mathematics"), ("D-Science","D-Science"), ("E-Language Other Than English","E-Language Other Than English"), ("F-Visual And Performing Arts","F-Visual And Performing Arts"), ("G-College-Preparatory Elective","G- College-Preparatory Elective")])
    course_difficulty = SelectField('Course Difficulty',choices=[("",""),("Advanced Placement (AP)","Advanced Placement (AP)"),("Honors (HP)", "Honors (HP)")])
    course_department = SelectField('Course Department',choices=[("Mathmatics","Mathmatics"),("Science", "Science"),("English", "English"),("Visual And Performing Arts", "Visual And Performing Arts"),("Humanities", "Humanities"),("Physical Education", "Physical Education"), ("World Languages", "World Languages"), ("Career Techincal Education", "Career Techincal Education"),("Other Elective","Other Elective")], validators=[DataRequired()] )
    submit = SubmitField('Add Course')

class TeacherCourseForm(FlaskForm):
    teacher = SelectField('Teacher',choices=[], validators=[DataRequired()]) 
    course = SelectField('Course',choices=[], validators=[DataRequired()])
    course_description = FileField('Course Description', validators=[DataRequired()])
    course_files = FileField("Insert Files Relevant To The Course (Ex. Syllabus, Examples of Coursework)", validators=[DataRequired()]) 
    submit = SubmitField('Add Class')

# Start building out the physical forms. Follow the process you used to create the school tag


