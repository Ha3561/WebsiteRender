from ToDo import app 
from flask import request, redirect, url_for, render_template

@app.route('/success')
def success_page():
    return 'Form submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)
