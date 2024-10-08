from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from connection1 import get_connection1
import os
from flask_bcrypt import Bcrypt 

from werkzeug.utils import secure_filename
bp = Blueprint('website', __name__, url_prefix='/')

UPLOAD_FOLDER = '/images'
# ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bcrypt = Bcrypt() 


@bp.route('/register', methods=['POST'])
def insert():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    hashed_password = bcrypt.generate_password_hash (password).decode('utf-8') 


    if not name or not email or not password:
        flash("all filed are  required")
        return redirect(url_for('register'))
    connection = get_connection1()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO data (name, email, password) VALUES (%s, %s, %s)", (name,email, password))
        connection.commit()
        flash("Registertation succesfully:")
        return redirect(url_for('/login'))

    except Exception as e:
        connection.rollback()
        flash("An error occurred: {}".format(e))
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('/login'))

@bp.route('/login',methods=['POST'])
def login():
    if request.method =='POST':
        email=request.form.get('email')
        password=request.form.get('password')

    if not email or not password:
        flash("Both field are required:")
        return redirect(url_for('/login'))
    connection=get_connection1()
    cursor=connection.cursor()

    try:
        cursor.execute('select password from data  where email=%s',(email))
        result=cursor.fetchone()
        if result:
            is_valid = bcrypt.check_password_hash(result[0], password)
            flash("Login suceefully:")
            return redirect(url_for('/home'))
        else:
            flash('Invalid email and password')
    except Exception as e:
        flash(" You need to register Before Login:")
        return redirect(url_for('register'))
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('/home')) 

# crud opeartion

@bp.route('/insert',methods=['POST'])
def insert():
   if request.method == 'POST':
        product_name=request.form.get('name')
        product_price=request.form.get('price')
        file=request.files.get('image')
        f = request.files['file'] 
        f.save(f.filename)

        connection=get_connection1()
        cursor=connection.cursor()
        cursor.execute("INSERT INTO DATA (name,price,image) VALUES (%s,%s,%s)",(product_name,product_price,file))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('home'))
   
@bp.route('/update/<int:id>',methods=['POST'])
def update(id):
    connection = get_connection1()
    cursor = connection.cursor()
    if request.method == 'POST':
        product_name=request.form.get('name')
        product_price=request.form.get('price')
        f = request.files.get('image')
        if f and f.filename:
            if allowed_file(f.filename):
                filename = secure_filename(f.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                f.save(file_path)
                cursor.execute("UPDATE data SET name=%s, price=%s, image=%s WHERE id=%s", (product_name, product_price, filename, id))
            else:
                flash('Invalid file type. Only JPG, JPEG, PNG, and GIF are allowed.')
        else:
            cursor.execute("UPDATE data SET name=%s, price=%s, image=%s WHERE id=%s", (product_name, product_price, f))
        
        connection.commit()
        cursor.close()
        connection.close()
        flash('Data updated successfully!')
        return redirect(url_for('index'))


 @bp.route('/delete/<int:id>',methods=['POST'])
 def delete(id):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute('delete from data where id=%s',(id,))
    connection.commit()
    cursor.close()
    connection.close()

@bp.route('/AddToCart/<int:id>',methods=['POST'])
def AddCart(id):
    connection = get_connection1()
    cursor = connection.cursor()
    if request.method == 'POST':
        product_name=request.form.get('name')
        product_price=request.form.get('price')
        f = request.files.get('image')
        




    










