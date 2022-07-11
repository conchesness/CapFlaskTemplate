# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask.app import Flask
from flask import flash
from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, NumberRange, Email, Optional, InputRequired, ValidationError, DataRequired, EqualTo
from wtforms.fields.html5 import URLField
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, HiddenField, IntegerField, SelectField, FileField, BooleanField
from app.classes.data import User

departments = [("",""),("Mathmatics","Mathmatics"),("Science", "Science"),("English", "English"),("Visual and Performing Arts", "Visual and Performing Arts"),("Humanities", "Humanities"),("PE", "Physical Education (PE)"), ("World Languages", "World Languages"), ("CTE", "Career Techincal Education (CTE)"),("Other Elective","Other Elective")]

class CourseFilterForm(FlaskForm):
    department = SelectField('Department',choices = departments)
    filter = SelectField("Filter",choices=[("",""),("Courses with Teachers","Courses with Teachers"),("Courses without Teachers","Courses without Teachers")])
    submit = SubmitField("Search")

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
    course_department = SelectField('Course Department',choices=departments)
    submit = SubmitField('Add Course')

class TeacherCourseForm(FlaskForm):
    teacher = SelectField('Teacher',choices=[],validate_choice=False)
    course = SelectField('Course',choices=[],validate_choice=False)
    course_description = StringField('Course Description')
    course_link = URLField("A link to a Google Document or a folder", validators=[URL()]) 
    submit = SubmitField('Submit')

# Start building out the physical forms. Follow the process you used to create the school tag


