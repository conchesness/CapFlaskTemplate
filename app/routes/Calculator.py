from app import app
from flask import render_template

@app.route('/calculator')
def calculator():
    # some code here
  return render_template('calculator.html')