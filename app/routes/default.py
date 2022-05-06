from app import app
from flask import render_template

# This is for rendering the home page
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/todolist')
def todolist():
    return render_template('todolist.html')

@app.route('/stressrelief')
def stressrelief():
    return render_template('stressrelief.html')

# @app.route('/timer')
# def timer():
#     return render_template('timer.html')