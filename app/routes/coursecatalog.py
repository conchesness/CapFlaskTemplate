from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Courses
from app.classes.forms import CoursesForm
from flask_login import login_required
import datetime as dt


@app.route('/course/<courseID>')
@login_required
def course(courseID):
    thisCourse = Courses.objects.get(id=courseID)
    return render_template('course.html',course=thisCourse)

@app.route('/course/list')
@login_required
def courseList():
    courses=Courses.objects()
    return render_template('courses.html',courses=courses)

# This route actually does two things depending on the state of the if statement 
# 'if form.validate_on_submit()'. When the route is first called, the form has not 
# been submitted yet so the if statement is False and the route renders the form.
# If the user has filled out and succesfully submited the form then the if statement
# is True and this route creates the new post based on what the user put in the form.
# Because this route includes a form that both gets and posts data it needs the 'methods'
# in the route decorator.
@app.route('/course/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def courseNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = CoursesForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new post form. 
        # Post() is a mongoengine method for creating a new post. 'newPost' is the variable 
        # that stores the object that is the result of the Post() method.  
        newCourse = Courses(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            course_number = form.course_number.data,
            course_title = form.course_title.data,
            course_name = form.course_name.data,
            course_ag_requirement = form.course_ag_requirement.data,
            course_difficulty = form.course_difficulty.data,
            course_department = form.course_department.data,
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
        )
        # This is a method that saves the data to the mongoDB database.
        newCourse.save()

        # Once the new post is saved, this sends the user to that post using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a post so we want 
        # to send them to that post. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('course',courseID=newCourse.id))

    return render_template('coursesform.html',form=form)

# This route enables a user to edit a post.  This functions very similar to creating a new 
# post except you don't give the user a blank form.  You have to present the user with a form
# that includes all the values of the original post. Read and understand the new post route 
# before this one. 
@app.route('/course/edit/<courseID>', methods=['GET', 'POST'])
@login_required
def courseEdit(courseID):
    editCourse = Courses.objects.get(id=courseID)
    # if the user that requested to edit this post is not the author then deny them and
    # send them back to the post. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editCourse.author:
        flash("You can't edit a course you don't own.")
        return redirect(url_for('course',courseID=courseID))
    # get the form object
    form = CoursesForm()
    # If the user has submitted the form then update the post.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editCourse.update(
            course_number = form.course_number.data,
            course_title = form.course_title.data,
            course_name = form.course_name.data,
            course_ag_requirement = form.course_ag_requirement.data,
            course_difficulty = form.course_difficulty.data,
            course_department = form.course_department.data,
            modify_date = dt.datetime.utcnow
        )
        # After updating the document, send the user to the updated post using a redirect.
        return redirect(url_for('course',courseID=courseID))

    # if the form has NOT been submitted then take the data from the editPost object
    # and place it in the form object so it will be displayed to the user on the template.
    form.course_number.data = editCourse.course_number
    form.course_title.data = editCourse.course_title
    form.course_name.data = editCourse.course_name
    form.course_ag_requirement.data = editCourse.course_ag_requirement
    form.course_difficulty.data = editCourse.course_difficulty
    form.course_department.data = editCourse.course_department


    # Send the user to the post form that is now filled out with the current information
    # from the form.
    return render_template('coursesform.html',form=form)

# This route will delete a specific post.  You can only delete the post if you are the author.
# <postID> is a variable sent to this route by the user who clicked on the trash can in the 
# template 'post.html'. 
# TODO add the ability for an administrator to delete posts. 
@app.route('/course/delete/<courseID>')
# Only run this route if the user is logged in.
@login_required
def courseDelete(courseID):
    # retrieve the post to be deleted using the postID
    deleteCourse = Courses.objects.get(id=courseID)
    # check to see if the user that is making this request is the author of the post.
    # current_user is a variable provided by the 'flask_login' library.
    if current_user == deleteCourse.author:
        # delete the post using the delete() method from Mongoengine
        deleteCourse.delete()
        # send a message to the user that the post was deleted.
        flash('The Post was deleted.')
    else:
        # if the user is not the author tell them they were denied.
        flash("You can't delete a post you don't own.")
    # Retrieve all of the remaining posts so that they can be listed.
    course = Courses.objects()  
    # Send the user to the list of remaining posts.
    return render_template('courses.html',courses=course)
