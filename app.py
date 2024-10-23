from flask import Flask, render_template, request
import DB


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = request.form.get('email')
        password = request.form.get('password') 
        # проверяем существует ли пользователь и создаём только если не существует DB.is_user_exist
        DB.create_user(login, password)
        # нужно добавить под формой вывод: успешная регистрация или пользователь с таким email уже зарегистрирован
    return render_template('registration.html')
    