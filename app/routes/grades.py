from sqlalchemy import delete
from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Grades
from app.classes.forms import GradesForm
from flask_login import login_required
import datetime as dt 

@app.route('/grades/new', methods=['GET', 'POST'])
@login_required
def GradesNew():
    form = GradesForm() 

    if form.validate_on_submit():
        newGrade = Grades(
            Course = form.Grade.data,
            Student = current_user.id,
            Grade = form.Grade.data,
            GradePoints = form.GradePoints.data
        )
        newGrade.save() 
        return redirect(url_for('gradeList'))

    return render_template('gradeform.html',form=form)

@app.route('/grade/edit/<gradeId>', methods=['GET', 'POST'])
@login_required
def gradesEdit(gradeId):
    form = GradesForm() 
    editGrade = Grades.objects.get(id = gradeId)

    if form.validate_on_submit():
        editGrade.update(
            Course = form.Course.data,
            Grade = form.Grade.data,
            GradePoints = form.GradePoints.data
        )
        return redirect(url_for('gradeList'))

    form.Grade.data = editGrade.Grade
    form.Course.data = editGrade.Course 
    form.GradePoints.data = editGrade.GradePoints
    
    return render_template('gradeform.html',form=form)

@app.route('/grade/<gradeId>')
@login_required
def grade(gradeId):
    thisGrade = Grades.objects.get(id = gradeId)
    return render_template('grade.html',grade = thisGrade)

@app.route('/grade/delete/<gradeId>')
@login_required
def gradeDelete(gradeId):
    deleteGrade = Grades.objects.get(id = gradeId)
    flash(f"Deleting grade.")
    deleteGrade.delete()
    return redirect(url_for('gradeList'))

@app.route('/grade/list')
@login_required
def gradeList():
    grades = Grades.objects()
    return render_template('grades.html',grades=grades)
