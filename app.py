from datetime import datetime
from wsgiref.validate import validator
from flask import Flask, jsonify, render_template,request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm 
from wtforms import StringField , SubmitField
from wtforms.validators import DataRequired 
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
import json
 
# Create a Flask Instance 
app = Flask(__name__)
app.config['SECRET_KEY'] = "What is my secrete key?"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/Flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 
migrate = Migrate(app, db)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)

# create Modal
class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable = False)
    email = db.Column(db.String(120), nullable = False,unique = True)
    date_added = db.Column(db.DateTime , default = datetime.utcnow)

    # Create a return ref
    def __repr__(self):
        return '<Name %r>' % self.name 

# Create a Validate WTForm 
class UserForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def index():
    # try :
    #     cur = mysql.connection.cursor()
    #     # cur.execute('''SELECT user, host FROM mysql.user''')
    #     cur.execute('''CREATE TABLE IF NOT EXIST todo(id int,name varchar(255))''')
    #     mysql.connection.commit()
    #     # rv = cur.fetchall()
    #     return "Hello world!!"
    # except:
    #     return "Alredy there table"
    return render_template('index.html')

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
def user(name):
    # name = "Joey Tribbani"
    return render_template('user.html',name=name)

@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form = UserForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Users(name=form.name.data,email=form.email.data)
            db.session.add(user)
            db.session.commit()
            flash("User Added Successfully!")

        else:
            flash("User Already Exist")

        name = form.name.data
        form.name.data = ''
        form.email.data = ''
    
    all_users = Users.query.order_by(Users.date_added)
   

    
    return render_template('name.html',
    form =form,
    name = name,
    all_users = all_users
    )

@app.route('/update/<id>',methods=['GET','POST'])
def update(id):
    update_form = UserForm()
    data_update = Users.query.get_or_404(id)
    

    if request.method == "POST":
        data_update.name = request.form['name']
        data_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User updated Successfully.")
            return render_template('update.html',
            form = update_form,
            data_update = data_update,
            )
        except:
            flash("Something went wrong Try again")
            return render_template('update.html',
            form = update_form,
            data_update = data_update,
            )
    else:
        # flash("User updated Successfully.")
        return render_template('update.html',
        form = update_form,
        data_update = data_update,
        )

@app.route('/user_update',methods=['GET','POST'])
def user_update():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        print(name," ---",email)
        flash("Hello there we are somethig {}".format(name))
        return render_template('user_form.html')
    else:
        flash("Direct call")
        return render_template('user_form.html')

@app.route('/delete/<id>',methods=['GET','POST'])
def delete(id):
    delete_form = UserForm()

    if request.method == "GET" or request.method == "POST":
        print(id,"---")
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(''' Delete from users where id = (%d) ''',(id))
            mysql.connection.commit()
            flash("User Deleted Successfully.")
            
        except Exception as e:
            
            flash(e)
        
        finally:
            all_users = Users.query.order_by(Users.date_added)
    

            return render_template('name.html',
            form =delete_form,
            all_users = all_users
            )

       
        
    else:
        print(id,"Delete")
        all_users = Users.query.order_by(Users.date_added)
    

        return render_template('name.html',
        form =delete_form,
        all_users = all_users
        )
   

@app.route('/testing')
def test():
    data = {'a':{"demo":[1,2,3]},'b':{"demo":[4,5,6]}}
    return json.dumps(data)

#  Fetch from Database 
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

# Variable as input
@app.route('/u/<name>')
def unmme(name):
    return "<h1>Hello {} .. how you doin!</h1>".format(name)


# Dyanamic Error handling 
@app.errorhandler(404)
def page_not_found(name):
    return "Error 404  "

@app.errorhandler(500)
def page_not_found(name):
    return "Error 500"

# Initiliazing of code
if __name__ == '__main__':
    app.run(debug=True)