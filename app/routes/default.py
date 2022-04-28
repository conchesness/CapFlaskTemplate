from app import app
from flask import render_template

# This is for rendering the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/todolist')
def todolist():
    return render_template('todolist.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')