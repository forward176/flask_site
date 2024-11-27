from flask import Flask, render_template, request
import DB
from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    context = {}
    context['output'] = ''
    if request.method == 'POST':
        login = request.form.get('email')
        password = request.form.get('password') 
        context['login'] = login
        context['password'] = password
        if not DB.is_user_exist(login):
            context['output'] = 'Такого пользователся не существует!'
        elif not DB.check_password(login, password):
            context['output'] = 'Неверный пароль!'
        else: 
            context['output'] = 'Успешный вход!'
            
            
    return render_template('index.html', context=context)
    


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    context = {}
    if request.method == 'POST':
        login = request.form.get('email')
        password = request.form.get('password')
        if not login:
            context['output'] = 'Введите логин!'
        elif not password:
            context['output'] = 'Введите Пароль!'
        elif DB.is_user_exist(login):
            context['output'] = 'Такой пользователь уже существует!'
        else:
            DB.create_user(login, password)
            context['output'] = 'Вы успешно зарегистрированы!'
    return render_template('registration.html', context=context)


@app.route('/levels', methods=['GET', 'POST'])
def levels():
    context = {}
    ###
    context['count_levels'] = 10
    context['passed_levels'] = 4
    ###
    return render_template('levels.html', context=context)
    

@app.route('/level')
def level():
    context = {}
    if 'lvl' in request.args:
        context['lvl'] = request.args.get('lvl')
        # проверки на существование уровня и доступность
        path = f'levels/{context["lvl"]}.lvl'
        mat = open(path, encoding="UTF-8").read().split()
        context["mat"] = mat
        return render_template('level.html', context=context)    
    else:
        return redirect(url_for('levels'), 301)
    