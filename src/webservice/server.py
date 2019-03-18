from flask import Flask, request
from src.webservice._user import User
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:irulez4database@10.0.50.50/iRulez'

db = SQLAlchemy(app)


@app.route('/user', methods=['GET', 'POST'])
def user_route():
    if request.method == 'GET':
        return User.get_all_users()
    elif request.method == 'POST':
        return User.create_new_user(request)


if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
