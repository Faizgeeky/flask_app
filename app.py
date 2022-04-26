from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import json

# Create a Flask Instance 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask'
db = SQLAlchemy(app)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'flask'
 
# mysql = MySQL(app)

@app.route('/')
def users():
    try :
        cur = mysql.connection.cursor()
        # cur.execute('''SELECT user, host FROM mysql.user''')
        cur.execute('''CREATE TABLE IF NOT EXIST todo(id int,name varchar(255))''')
        mysql.connection.commit()
        # rv = cur.fetchall()
        return "Hello world!!"
    except:
        return "Alredy there table"

@app.route('/login')
def login():
    # if request.method == 'GET':
    #     return "Login via the login Form"
    
    if request.method == 'GET':
        data = request.args # ['id']
        # print("Data ---",data['id'])
        id = data['id']
        name = data['name']
        print("Name",name ,' ID',id)
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO todo VALUES(%s,%s)''',(id,name))
        mysql.connection.commit()
        cursor.close()
        return f"Done"



@app.route('/user/<name>')
def hello_world(name):
    return render_template('index.html',u_name = name)

@app.route('/demo')
def demo():
    return 'Hi there'

@app.route('/view')
def view_data():
    try :
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * from todo''')
        data = cursor.fetchall()
        data = json.dumps(data)
        print("Data ---",data)
        cursor.close()
        return data, 201
    
    except Exception as e:
        print(e)

@app.route('/u/<name>')
def unmme(name):
    return "<h1>Hello {} .. how you doin!</h1>".format(name)

@app.errorhandler(404)
def page_not_found(name):
    return "Error 404  "

@app.errorhandler(500)
def page_not_found(name):
    return "Error 500"

if __name__ == '__main__':
    app.run(debug=True)