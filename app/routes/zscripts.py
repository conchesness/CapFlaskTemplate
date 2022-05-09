from flask.helpers import url_for
from flask_login import current_user
from app import app
from flask import render_template, redirect, flash
from app.classes.data import User, Courses, TeacherCourse
import pandas as pd
import datetime as dt
from mongoengine.errors import NotUniqueError, DoesNotExist
from mongoengine import Q

@app.route('/coursesimport')
def coursesimport():
    # Place a csv file of the courses to be imported into the csv 
    # folder at the root level. name the file 'courses.csv' and name all
    # the columns to match the names in the courses data document.

    # This reads the csv file in to a pandas dataframe
    df_courses = pd.read_csv('csv/courses.csv', encoding = "ISO-8859-1")
    # Pandas turns all blanks in to 'NA', this replaces the 'NA' with blanks.
    df_courses.fillna('', inplace=True)

    #  This turns that dataframe in to a python dictionary
    courses = df_courses.to_dict(orient='records')
    length = len(courses)

    # this for loop iterates through all of the courses and first looks to 
    # see if the course exists in the database.  If it does, it will update it.
    # If it doesn't, it will create a new one.
    for i,course in enumerate(courses):
        try:
            thisCourse = Courses.objects.get(course_number=course['course_number'])
        except DoesNotExist:
            thisCourse = False
        else:
            thisCourse.update(
                course_number = course['course_number'],
                course_title = course['course_title'],
                course_name = course['course_name'],
                course_ag_requirement = course['course_ag_requirement'],
                course_difficulty = course['course_difficulty'],
                course_department = course['course_department'],
                modify_date = dt.datetime.utcnow 
            )
        if not thisCourse:
            newCourse = Courses(
                course_number = course['course_number'],
                course_title = course['course_title'],
                course_name = course['course_name'],
                course_ag_requirement = course['course_ag_requirement'],
                course_difficulty = course['course_difficulty'],
                course_department = course['course_department'],
                modify_date = dt.datetime.utcnow 
            )
            newCourse.save()
        print(f"importing {i}/{length}: {course['course_number']} ")
    return redirect(url_for('index'))

@app.route('/importteachers')
def importteachers():
    df_teachers = pd.read_csv('csv/teachers.csv', encoding = "ISO-8859-1")
    df_teachers.fillna('', inplace=True)
    teachers = df_teachers.to_dict(orient='records')
    length = len(teachers)
    for i,teacher in enumerate(teachers):
        try:
            thisTeacher = User.objects.get(teacher_number=teacher['teacher_number'])
            print('Teacher exists.')
        except:
            thisTeacher = False
            print("Teacher doesn't exist")
        else:
            thisTeacher.update(
                teacher_number = teacher['teacher_number'],
                email = teacher['email'],
                fname = teacher['fname'],
                lname = teacher['lname'],
                role = 'Teacher',
                troom_number = teacher['troom_number']
            )
            print(f"{i}/{length}: Updating {teacher['fname']} {teacher['lname']}")
        if not thisTeacher:
            newTeacher = User(
                teacher_number = teacher['teacher_number'],
                email = teacher['email'],
                fname = teacher['fname'],
                lname = teacher['lname'],
                role = 'Teacher',
                troom_number = teacher['troom_number']
            )
            newTeacher.save()
            print(f"{i}/{length}: Creating {teacher['fname']} {teacher['lname']}")
        
    return redirect(url_for('index'))

@app.route('/importteachercourses')
def importteachercourses():
    df_teachercourses = pd.read_csv('csv/teachercourses.csv', encoding = "ISO-8859-1")
    df_teachercourses.fillna('', inplace=True)
    teachercourses = df_teachercourses.to_dict(orient='records')
    length = len(teachercourses)
    for i,tcourse in enumerate(teachercourses):
        importProceed=True
        try:
            course = Courses.objects.get(course_number = tcourse['course_number'])
        except:
            print(f"course {tcourse['course_number']} doesn't exist. ")
            importProceed = False
        try:
            teacher = User.objects.get(teacher_number = tcourse['teacher_number'])
        except:
            print(f"Teacher {tcourse['teacher_number']} doesn't exist. ")
            importProceed = False
        if importProceed:
            query = Q(course = course) and Q(teacher=teacher)
            try:
                thisTeacherCourse = TeacherCourse.objects.get(query)
            except:
                newTeacherCourse = TeacherCourse(
                    teacher = teacher,
                    course = course,
                    teachercourseid = f"{teacher.teacher_number}-{course.course_number}" 
                )
                newTeacherCourse.save()
                print(f"{i}/{length}: Created TeacherCourse {teacher.fname} {teacher.lname} {course.course_title}")
            else:
                print(f"{i}/{length}: Already exists TeacherCourse {teacher.fname} {teacher.lname} {course.course_title}.")
    return redirect(url_for('index'))