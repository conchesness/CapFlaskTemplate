from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Courses, Comment, TeacherCourse
from app.classes.forms import CoursesForm, CommentForm, CourseFilterForm
from flask_login import login_required
import datetime as dt


@app.route('/course/<courseID>')
@login_required
def course(courseID):
    thisCourse = Courses.objects.get(id=courseID)
    theseComments = Comment.objects(course=thisCourse)
    teacherCourses = TeacherCourse.objects(course = thisCourse)
    return render_template('course.html',course=thisCourse, comments=theseComments, teacherCourses=teacherCourses)

@app.route('/course/list',methods=["GET","POST"])
@login_required
def courseList():
    courses=Courses.objects()
    form = CourseFilterForm()
    if form.validate_on_submit():
        courses = Courses.objects(course_department = form.department.data)
    return render_template('courses.html',courses=courses,form=form)

@app.route('/course/new', methods=['GET', 'POST'])
@login_required
def courseNew():
    form = CoursesForm()

    if form.validate_on_submit():

        newCourse = Courses(
            course_number = form.course_number.data,
            course_title = form.course_title.data,
            course_name = form.course_name.data,
            course_ag_requirement = form.course_ag_requirement.data,
            course_difficulty = form.course_difficulty.data,
            course_department = form.course_department.data,
            author = current_user.id,
            modify_date = dt.datetime.utcnow
        )
        newCourse.save()

        return redirect(url_for('course',courseID=newCourse.id))

    return render_template('coursesform.html',form=form)


@app.route('/course/edit/<courseID>', methods=['GET', 'POST'])
@login_required
def courseEdit(courseID):
    editCourse = Courses.objects.get(id=courseID)
    if not current_user.isadmin:
        flash("You can't edit a course unless you are an admin.")
        return redirect(url_for('course',courseID=courseID))
    form = CoursesForm()
    if form.validate_on_submit():
        editCourse.update(
            course_number = form.course_number.data,
            course_title = form.course_title.data,
            course_name = form.course_name.data,
            course_ag_requirement = form.course_ag_requirement.data,
            course_difficulty = form.course_difficulty.data,
            course_department = form.course_department.data,
            modify_date = dt.datetime.utcnow
        )
        return redirect(url_for('course',courseID=courseID))

    form.course_number.data = editCourse.course_number
    form.course_title.data = editCourse.course_title
    form.course_name.data = editCourse.course_name
    form.course_ag_requirement.data = editCourse.course_ag_requirement
    form.course_difficulty.data = editCourse.course_difficulty
    form.course_department.data = editCourse.course_department

    return render_template('coursesform.html',form=form)

@app.route('/course/delete/<courseID>')
@login_required
def courseDelete(courseID):
    deleteCourse = Courses.objects.get(id=courseID)
    if current_user == deleteCourse.author or current_user.isadmin:
        flash(f'The Course {deleteCourse.course_title} is being deleted.')
        deleteCourse.delete()
    else:
        flash("You can't delete a post you don't own.")
    course = Courses.objects()  
    return render_template('courses.html',courses=course)


@app.route('/course/search')
def courseSearch():
    form = CourseFilterForm()


@app.route('/comment/new/<courseID>', methods=['GET', 'POST'])
@login_required
def commentNew(courseID):
    course = Courses.objects.get(id=courseID)
    form = CommentForm()
    if form.validate_on_submit():
        newComment = Comment(
            author = current_user.id,
            course = courseID,
            content = form.content.data
        )
        newComment.save()
        return redirect(url_for('course',courseID=courseID))
    return render_template('commentform.html',form=form,course=course)

@app.route('/comment/edit/<commentID>', methods=['GET', 'POST'])
@login_required
def commentEdit(commentID):
    editComment = Comment.objects.get(id=commentID)
    if current_user != editComment.author:
        flash("You can't edit a comment you didn't write.")
        return redirect(url_for('post',courseID=editComment.course.id))
    course = Courses.objects.get(id=editComment.course.id)
    form = CommentForm()
    if form.validate_on_submit():
        editComment.update(
            content = form.content.data,
            modify_date = dt.datetime.utcnow
        )
        return redirect(url_for('course',courseID=editComment.course.id))

    form.content.data = editComment.content

    return render_template('commentform.html',form=form,course=course)   

@app.route('/comment/delete/<commentID>')
@login_required
def commentDelete(commentID): 
    deleteComment = Comment.objects.get(id=commentID)
    deleteComment.delete()
    flash('The comments was deleted.')
    return redirect(url_for('course',courseID=deleteComment.course.id)) 

@app.route('/teachercourse/<tcid>')
@login_required
def teachercourse(tcid):
    thisTC = TeacherCourse.objects.get(id=tcid)
    return render_template("teachercourse.html",tCourse = thisTC)