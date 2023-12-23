import re
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__,template_folder='template')
app.config['SECRET_KEY'] = 'super secret key'
@app.route("/")
def loadPage():
    return render_template('lead_form.html')


def is_valid_name(name):
    return bool(re.match("^[a-zA-Z]+$", name))

def is_valid_email(email):
    return bool(re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))

def is_valid_phone(phone):
    return bool(re.match("^[0-9]{10}$", phone))

def is_valid_password(password):
    return bool(re.match("^(?=.*[a-zA-Z])(?=.*[0-9!@#$%^&*(),.?\":{}|<>]).{1,12}$", password))

@app.route('/', methods=['POST'])
def lead_generation_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate form data
        if not name or not email or not phone or not password or not confirm_password:
            flash('All fields are required', 'error')
        if not is_valid_name(name):
            flash('Invalid name. Please use only alphabets.', 'error')

        if not is_valid_email(email):
            flash('Invalid email format.', 'error')

        if not is_valid_phone(phone):
            flash('Invalid Indian phone number. Please enter a 10-digit number.', 'error')

        if not is_valid_password(password):
            flash('Invalid password. Please use a combination of alphanumeric and special characters (max 12 characters).', 'error')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
        
        else:
            flash('Lead generated successfully!', 'success')
    return render_template('lead_form.html')


if __name__ == '__main__':
    app.run(debug=True)
