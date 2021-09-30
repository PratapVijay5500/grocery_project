from flask import Flask, render_template, request, jsonify, redirect, session
from sql_connection import get_sql_connection
import json
import products_dao
import orders_dao
import uom_dao
import os
import customer_order_details
# cursor = get_sql_connection()
app = Flask(__name__)

app.secret_key = os.urandom(24)
connection = get_sql_connection()

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect('/admin')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/register')
def register():
    return render_template('user.html')




@app.route('/getUOM', methods=['GET'])
def get_unit():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getProducts', methods=['GET'])
def get_products():
    product = products_dao.get_all_products(connection)
    response = jsonify(product)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id,
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route('/getCustomerOrders', methods=['GET'])
def get_customer_orders():
    response = customer_order_details.get_customer_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/edit', methods=['POST'])
def edit_product():

    return render_template('edit.html')

@app.route('/deleteCustomer', methods=['POST'])
def delete_customer():
    id = orders_dao.delete_customer(connection, request.form['order_id'])
    response = jsonify({
        'order_id': id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response





@app.route('/manageProduct')
def manageProduct():
    return render_template('manage-product.html')

@app.route('/order')
def order():
    return render_template('order.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    cursor = connection.cursor()
    email = request.form.get('email')
    password = request.form.get('password')

    query = ("""SELECT * FROM users WHERE email LIKE '{}' AND password LIKE '{}' """.format(email, password))
    cursor.execute(query)
    users = cursor.fetchall()
    if len(users) > 0:
        session['user_id']=users[0][0]
        return redirect('/')
    else:
        return redirect('/admin')

@app.route('/add_users', methods=['POST'])
def add_users():
    cursor = connection.cursor()
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    query = ("""INSERT INTO users (user_id, name, email, password) VALUES(NULL, '{}', '{}', '{}')"""
             .format(name, email, password))
    cursor.execute(query)
    connection.commit()

    query = ("""SELECT * FROM users WHERE email LIKE '{}'""".format(email))
    cursor.execute(query)
    myuser = cursor.fetchall()
    session['user_id'] = myuser[0][0]
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/admin')

@app.route('/login')
def login():
    session.pop('user_id')
    return redirect('/admin')


if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(debug=True,port=5000)