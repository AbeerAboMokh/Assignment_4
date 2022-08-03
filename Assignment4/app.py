from flask import Flask, redirect, url_for, render_template, request, session, jsonify, Blueprint
from datetime import timedelta
import mysql.connector
import requests

app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="assignment4"
)

# get all users from the database
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM users")
results = mycursor.fetchall()
assignment4_users = {}
for index, result in enumerate(results):
    key = "user{}".format(index)
    assignment4_users[key] = {"email": result[1], "name": result[2], "user_name": result[3], "age": result[4]}

@app.route('/')
def first_page():  # put application's code here
    return redirect(url_for('display_home_page'))


@app.route('/home')
def display_home_page():  # put application's code here
    return render_template('home.html')


@app.route('/contact')
def display_contact_us():  # put application's code here
    return render_template('contact.html')


@app.route('/assignment3_1')
def display_hobbies_page():
    the_hobbies = ('Writing', 'Dancing', 'basketball')
    return render_template('assignment3_1.html',
                           hobbies_dic=the_hobbies,
                           no_hobbies_message='Ops, there is no hobbies to display!')

def get_users():
    # get all users from the database
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")
    results = mycursor.fetchall()
    users = []
    for index, result in enumerate(results):
        users.append({"email": result[1], "name": result[2], "user_name": result[3], "age": result[4]})
    return users

@app.route('/assignment4', methods=['GET'])
def display_assignment4():
    return render_template('assignment4.html', users=get_users())

@app.route('/assignment4', methods=['POST'])
def add_user_assignment4():
    # get the form data
    data = request.form
    # Check what is the provided method
    method = data['method']

    # a message to return to the client
    message = 'Something is wrong'

    mycursor = mydb.cursor()

    # if the method is insert this means that the user is trying to insert a user
    if method == 'INSERT':
        # Get the form data
        email = data['email']
        name = data['name']
        user_name = data['user_name']
        age = data['age']

        # Build the SQL query
        sql = "INSERT INTO users (email, name, user_name, age) VALUES (%s, %s, %s, %s)"
        val = (email, name, user_name, age)

        # excute and commit the query
        mycursor.execute(sql, val)
        mydb.commit()

        # if the operation was done successfully
        if mycursor.rowcount:
            message = 'Inserted user successfully'
        # if the operation failed
        else:
            message = 'Failed to insert user'
    if method == 'UPDATE':
        # Get the form data
        email = data['email']
        name = data['name']
        age = data['age']

        mycursor = mydb.cursor()
        # Build the SQL query
        sql = "UPDATE users SET name = '{}', age = '{}' WHERE email = '{}'".format(name, age, email)
        
        # excute and commit the query
        mycursor.execute(sql)
        mydb.commit()

        # if the operation was done successfully
        if mycursor.rowcount:
            message = 'Updated user successfully'
        # if the operation failed
        else:
            message = 'Failed to update user'
    if method == 'DELETE':
        # Get the form data
        email = data['email']
        mycursor = mydb.cursor()
        
        # Build the SQL query
        sql = "DELETE FROM users WHERE email = '{}'".format(email)
        
        # excute and commit the query
        mycursor.execute(sql)
        mydb.commit()

        # if the operation was done successfully
        if mycursor.rowcount:
            message = 'Deleted user successfully'
        # if the operation failed
        else:
            message = 'Failed to delete user'

    # get all users from the database after the operation
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")
    results = mycursor.fetchall()

    # Prepare the output
    assignment4_users = {}
    for index, result in enumerate(results):
        key = "user{}".format(index)
    assignment4_users[key] = {"email": result[1], "name": result[2], "user_name": result[3], "age": result[4]}
    return render_template('assignment4.html', users=get_users(), message=message)

@app.route('/assignment4/users', methods=['GET'])
def get_users_json():
    # Get all the users from the database and return them as json
    return jsonify(get_users())

@app.route('/assignment4/outer_source', methods=['GET'])
def get_users_json_outer_source():
    return render_template('assignment4_2.html')

# Backend to get user name using requests
@app.route('/assignment4/outer_source', methods=['POST'])
def get_user_json_outer_source_request():
    # get the form data
    data = request.form
    # Check what is the provided method
    user_id = data['ID']
    response = requests.get("https://reqres.in/api/users/{}".format(user_id))
    user = response.json()
    user_data = user['data']
    user_name = user_data['first_name']
    email = user_data['email']
    return render_template('assignment4_2.html', name=user_name, email=email)

@app.route('/assignment4/restapi_users/', methods=['GET'])
def get_users_json_restful_default():
    # Return a default user
    return {
            "id": "id",
            "email": "email",
            "name": "name",
            "user_name": "user_name",
            "age": "age"
        }

@app.route('/assignment4/restapi_users/<user_id>', methods=['GET'])
def get_users_json_restful(user_id):
    try:
        # Try to convert the number to int
        int(user_id)
    except ValueError:
        # If we got an error then the value is not a number
        return {
            "error": "The id is not a number"
        }

    # Search for the username
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users WHERE id = {}".format(user_id))
    user = mycursor.fetchone()

    # If the user is found then user is not None
    if user is not None:
        return {
            "id": user[0],
            "email": user[1],
            "name": user[2],
            "user_name": user[3],
            "age": user[4]
        }
    else:
        # Return an error that the user was not found
        return {
            "error": "User was not found"
        }


users = {
    "user1": {"name": "ahmd", "email": "ahmd@gmail.com", "user_name": "El ahmad", "age": "20"},
    "user2": {"name": "abeer", "email": "abeer@gmail.com", "user_name": "El abeer", "age": "21"},
    "user3": {"name": "thaer", "email": "thaer@gmail.com", "user_name": "El thaer"},
    "user4": {"name": "Messi", "email": "Messi@gmail.com", "user_name": "El Messi"},
    "user5": {"name": "roaa", "email": "roaa@gmail.com", "user_name": "El roaa"}
}

user_data = {
    'El ahmad': '123',
    'El abeer': '125',
    'El thaer': '126',
    'El Messi': '127',
    'El roaa': '128',
}


@app.route('/assignment3_2', methods=['GET', 'POST'])
def display_users_page():  # put application's code here
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        if user_name in user_data:
            user_password = user_data[user_name]
            if user_password == password:
                session['user_name'] = user_name
                session['loged_in'] = True
                return render_template('assignment3_2.html',
                                       message='hi:)',
                                       user_name=user_name)
            else:
                return render_template('assignment3_2.html',
                                       message='The pass is Wrong!!')
        else:
            return render_template('assignment3_2.html',
                                   message=' sign in :)!')
    else:
        if 'name' in request.args:
            name = request.args["name"]
            if name == '':
                return render_template('assignment3_2.html', users=users)
            details = None
            for user_name in users.values():
                if user_name['name'] == name:
                    details = user_name
                    break
            if details:
                return render_template('assignment3_2.html',
                                       name=details['name'],
                                       email=details['email'],
                                       user_name=details['user_name']
                                       )
            else:
                return render_template('assignment3_2.html',
                                       no_user_message='No user found!!')
        return render_template('assignment3_2.html')


@app.route('/log_out')
def logout_func():
    session['loged_in'] = False
    session.clear()
    return redirect(url_for('display_users_page'))


@app.route('/session')
def session_func():
    return jsonify(dict(session))


if __name__ == '__main__':
    app.run()
