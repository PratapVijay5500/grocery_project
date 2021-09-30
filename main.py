from flask import Flask, render_template,request
import mysql.connector
app = Flask(__name__)
conn = mysql.connector.connect(host='127.0.0.1', user='root', password="72841990", database='grocery_store' )
cursor = conn.cursor()


@app.route('/')
def home():
    return render_template('admin.html')


@app.route('/register')
def register():
    return render_template('user.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/manageProduct')
def manageProduct():
    return render_template('manage-product.html')

@app.route('/order')
def order():
    return render_template('order.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    query = ("""SELECT * FROM users WHERE email LIKE '{}' AND password LIKE '{}' """.format(email, password))
    cursor.execute(query)
    users = cursor.fetchall()
    if len(users)>0:
        return render_template('index.html')
    else:
        return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)